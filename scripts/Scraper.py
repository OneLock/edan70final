import os
import re
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from scripts.util import make_directory, fetch_page,  save_json
from multiprocessing import Pool
import threading

class Scrapper:
    def __init__(self, directory, edition, url):
        self.directory = os.path.join(directory,str(edition))
        self.editions = {1: 2, 2: 4, 4 :6}
        self.edition = self.editions[edition]
        self.base_url = f'{url}/nf'
        self.download_url = f"{url}/download.pl"
        self.err_msg = '<p>Please return later and try again.'
        self.err_msg_idx = [2602, 2640]
        self.volumes = []
        self.links = []
        
        self.initialize()

    def initialize(self):
        make_directory(self.directory)
        self.get_links()
        self.download_files()
        self.make_table_content()
        
    def get_links(self):
        """
        Retrieves and extracts links from a web page.

        Returns:
            None
        """
        resp = fetch_page(self.base_url)

        soup = BeautifulSoup(resp, 'html.parser')
        e2_table = soup.findAll('table')[4]

        for tr in e2_table.findAll('tr')[2:]:
            self.extract_table_data(tr)
        self.links = [volume['url'] for volume in self.volumes]

    def make_table_content(self):
        """
        Generates the table content for the Scraper class.

        This method creates the table content by performing the following steps:
        1. Sets the directory path for the table of contents (TOC) files.
        2. Constructs the file path for the TOC JSON file.
        3. Creates the directory for the TOC files if it doesn't exist.
        4. Constructs the URL and style for the table of contents.
        5. Checks if the TOC directory is empty.
        6. If the directory is empty, processes all pages to generate the TOC and saves it as a JSON file.
        7. If the directory is not empty, prints a message indicating that the TOC file already exists.

        Returns:
            None
        """
        dir = "data/json/toc"
        toc_file = f'{dir}/toc.json'
        
        make_directory("data/json/toc")
        
        

        if toc_file[-8:] not in os.listdir(dir):
            self.process_all_pages()
            save_json(toc_file, self.toc)
        else:
            print(f"`{toc_file[-8:]}` already exists")
    
    def extract_table_data(self, tr):
        """
        Extracts data from a table row and appends it to the 'volumes' list.

        Args:
            tr (BeautifulSoup.Tag): The table row element containing the data.

        Returns:
            None
        """
        td = tr.findAll('td')[:4]
        year = td[0].get_text()
        _url = td[1].a.get('href')[3:-1]
        range = tuple(td[1].a.contents[0].split(' - '))

        rate = td[-1].get_text()
        if rate.endswith('%'):
            rate = rate.replace('%', '').replace(',', '.').strip()
        else:
            rate = 1.0
        entry =  {'published': year,'url': _url, 'range': range, 'index_rate': rate}
        self.volumes.append(entry)

    def extract_toc_entries(self, url, start_tag):
        """
        Extracts table of contents (TOC) entries from a given URL.

        Args:
            url (str): The URL to scrape the TOC entries from.
            start_tag (BeautifulSoup.Tag): The starting tag to search for TOC entries.
            
        Returns:
            None

        """
        style = 'text-decoration: none; color: black'
        contents = []
        for sibling in start_tag.find_next_siblings('a', style=style):
            
            match = sibling.find_all('a', style=style)
            nested_tags = []
            
            if match:
                nested_tags =  [sibling.text for sibling in match]
                
            if nested_tags:
                contents.extend(nested_tags)
            else:
                contents.append(sibling.text)
        self.toc[url] = contents

    def process_page(self, entry):
        """
        Process a page given an entry.

        Args:
            entry (dict): The entry containing information about the page.

        Returns:
            None

        Raises:
            None
        """
        url = entry['url']
        page_url = f'{self.base_url}{url}'
        
        self.toc[url] = []
            
        if 'supplement' in entry['range'][0].lower():
            pattern = entry['range'][0].split(' ')
            pattern = [pattern[0].capitalize(), pattern[1][0]]
            pattern = " ".join(pattern)
        else:
            pattern = entry['range'][0][0]
        
        resp = fetch_page(page_url)
        start_tag = BeautifulSoup(resp, 'html.parser') \
            .body \
            .find('h2', text=pattern)
            
        if start_tag:
            self.extract_toc_entries(url, start_tag)

    from tqdm import tqdm

    def process_all_pages(self):
        """
        Process all pages and return a table of contents (toc) dictionary.

        Returns:
            dict: A dictionary containing the table of contents for each page.

        """
        self.toc = {}
        
        def process_entry(entry, pbar):
            url = entry['url']
            self.process_page(entry)

            if url == "ci":
                idx = self.toc[url].index(entry['range'][1])
                self.toc[url] = self.toc[url][:idx+1]
            pbar.update()

        threads = []
        
        with tqdm(total=len(self.volumes)) as pbar:
            for volume in self.volumes:
                t = threading.Thread(target=process_entry, args=(volume, pbar))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            
    def download_files(self):
        """
        Downloads files from the specified links and saves them to the directory.

        Returns:
            None

        Raises:
            None
        """
        saved_files = [file[:-4] for file in os.listdir(self.directory)]
        q = list(set(self.links).difference(saved_files))
        
        total_files = len(q)  # Total number of files to process
        
        if total_files == len(self.links):
            print("No new files to download.")
        else:
            with tqdm(total=total_files, desc=f"Downloading {total_files} Files") as pbar:
                while q:
                    link = f"nf{q.pop(0)}"  # Pop the first element
                    payload = {"mode": "ocrtext", "work": link}
                    url = f"{self.download_url}/{link}"
                    # Construct URL
                    text = fetch_page(url, payload)
                    
                    
                    # Check for error message
                    err = text.find(self.err_msg, *self.err_msg_idx) > 0
                    if err:
                        print(err)
                        q.append(link[2:])
                        time.sleep(1)
                        continue
                    # remove all text until first article
                    regex = r"REALENCYKLOPEDI"
                    matches = list(re.finditer(regex, text, re.MULTILINE))
                    start = 0
                    
                    if not matches:
                        if 'bn' in link:
                            start = text.index("<b>Kikarsikte")
                        if 'bo' in link:
                            start = text.index("<b>Kromat")
                    else:
                        start = matches[-1].end()
                    text = "\n\n" + text[start:]   
                    
                    # Write response to file                        
                    file_path = os.path.join(self.directory, link[2:] + ".txt")
                    with open(file_path, "w") as f:
                        f.write(text)
                    
                    # Update progress bar
                    pbar.update(1)  # Increment progress by 1
                    pbar.set_postfix({"File": file_path})