import cProfile
import pstats
import argparse
import json
from scripts.Scraper import Scrapper
from scripts.Segmenter import Segmenter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', help='Uggleupplagan')
    parser.add_argument('-c', action='store_true', help='Running the classifier')
    parser.add_argument('-e', action='store_true', help='Evaluating the classifier')
    parser.add_argument('-m', action='store_true', help='Generating a map visualization')
    args = parser.parse_args()

    with open('settings.json') as f:
        _config = json.load(f)[0]

    if args.s:
        config = _config['scraper']
        edition = int(config['edition']) 
        rootdir = config['rootdir']
        url = config['url']

        sc = Scrapper(rootdir, edition, url)
        sg = Segmenter(_config['segmenter'])
       

    # if args.a:
    #     print('Annotating selected')
    #     annotator.get_and_save_coords(config)
        
    # if args.c:
    #     print('Running the classifier selected')
    #     classifier.run(config)

    # if args.e:
    #     print('Evaluating the classifier selected')
    #     classifier.evaluate(config)

    #if args.r:
        #TODO print("Classifier REPL selected")

    # if args.m:
    #     print('Generating a visualization selected')
    #     visualization.twod_map_coords(config)

    if not any(vars(args).values()):
        parser.print_help()

if __name__ == '__main__':
    main()