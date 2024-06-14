import cProfile
import pstats
import argparse
import json
from scripts.Scraper import Scrapper
from scripts.Segmenter import Segmenter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', help='Uggleupplagan')
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

    if not any(vars(args).values()):
        parser.print_help()

if __name__ == '__main__':
    main()
