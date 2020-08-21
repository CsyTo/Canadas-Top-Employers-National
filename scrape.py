import sys
import os
import argparse
import logging
from datetime import datetime
from scripts.main import *
from scripts.helpers import *

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(message)s')

def parse_args():
    parser =  argparse.ArgumentParser()
    parser.add_argument('alias')
    return vars(parser.parse_known_args()[0])

def main():
    args = parse_args()
    FileHelper.make_tmp()
    eval(args['alias'])("CanadasTop100_National",args['alias']).call()

if __name__ == '__main__':
    main()
