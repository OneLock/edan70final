import difflib
import os
import regex as re

from tqdm import tqdm
from scripts.util import make_directory, open_file, save_json
from fuzzywuzzy import process

class Segmenter:
    def __init__(self, *args):
        self.inputDirectory = args[0]['input_dir']
        self.segmentedDirectory = args[0]['segmentedDirectory']
        self.segmentedFilePath = args[0]['segmentedFile']
        self.paragraphIndexFile = args[0]['paragraphIndexesFile']
        self.toc_file = args[0]['toc_file']
        
        self.patterns = [
            r'^<b>.*',
            r"\s*\b\d+\.\s*<sp>\s*\w{1}[^<>]*",
            r"\s\d{1,2}\.\s\w+",
            r"\d{1,2}\.\s+<i>.*",
        ]
        
        self.initialize()
    
    def initialize(self):
        self.toc = open_file(self.toc_file, 'json')
        self.links = list(self.toc.keys())
        self.paragraphIndexes = {k: [] for k in self.links}
        
        self.segment()
        
            
    def segment(self):
        make_directory(self.segmentedDirectory)
        if self.paragraphIndexFile not in os.listdir(self.segmentedDirectory):
            self.findParagraphsIndexes()
            path = os.path.join(self.segmentedDirectory, self.paragraphIndexFile)
            save_json(path, self.paragraphIndexes)
            
        if self.segmentedFilePath not in os.listdir(self.segmentedDirectory):
            if not self.paragraphIndexes['ba']:
                path = os.path.join(self.segmentedDirectory, self.paragraphIndexFile)
                self.paragraphIndexes = open_file(path, 'json')
            self.process_articles()
            
        else:
            print("Segmentation already done!")


    def findParagraphsIndexes(self):
        for volume in tqdm(self.links, desc="Segmenting in progress", total=len(self.links)):
            fp = os.path.join(self.inputDirectory, f"{volume}.txt")
            
            with open(fp, 'r') as file:
                content = file.read()

            paragraphs = [p for p  in content.split('\n\n') if len(p) > 10 ]
            
            for articleNumber, paragraph in enumerate(paragraphs):
                lines = paragraph.split('\n')
                # print({'prev': prev,'curr': curr})
                for line in lines:
                    found = 0
                    
                    if not line:
                        continue
                    
                    for pattern in self.patterns:
                        if re.match(pattern, line):
                            found = 1
                            self.paragraphIndexes[volume].append((articleNumber, line))
                            break
                    
                    if found:
                        break
                    
                    if not found and re.search(r'\w', line): 
                        idx  = max(0, len(self.paragraphIndexes[volume])-1)
                        r = difflib.get_close_matches(line, self.toc[volume][idx: idx+200], cutoff=0.70)
                        
                        if not r and len(line) > 10:
                            r = process.extractBests(line, self.toc[volume][idx : idx+5], score_cutoff=95)

                        if r :
                            self.paragraphIndexes[volume].append((articleNumber, line))
                        break

    def extract_headword(self, line):
        headword = re.sub(r'<.*?>', '', line )
        p =  r"[^[[:punct:]\d\s]+"
        match = re.search(p, headword)
        if match:
            return headword[match.start():]
        return headword
    
    def process_articles(self):
        self.articles = []
        print("Processing articles")
        for fileNum, volume in enumerate(self.links, start=1):
            fp = os.path.join(self.inputDirectory, f"{volume}.txt")
            with open(fp, 'r') as file:
                content = file.read()

            paragraphs = [p for p  in content.split('\n\n') if len(p) > 10 ]

            volumeIndexes = self.paragraphIndexes[volume]
            length =  len(volumeIndexes)
            
            for articleNum in range(length):
                s,hw = volumeIndexes[articleNum]
                hw = self.extract_headword(hw)
                e = None if articleNum+1 == length else volumeIndexes[articleNum+1][0]
                
                article = paragraphs[s:e]
                line = [l for l in article[0].split('\n') if l]
                
                if len(line):
                    line = line[0]

                    
                txt  =  "\n\n".join(article)
                eid =  f'v{fileNum}-{articleNum+1}-0'
                lbl = None
                QID = None
                
                a = {'headword': hw, 'text': txt, 'entryid': eid, 'label': lbl,'QID': QID}
                self.articles.append(a)
                
        path = os.path.join(self.segmentedDirectory, self.segmentedFilePath)
        save_json(path, self.articles)    