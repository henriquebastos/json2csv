import argparse
import json
from pprint import pprint

from . import flatten

parser = argparse.ArgumentParser('json2csv')
parser.add_argument('input', type=argparse.FileType())
parser.add_argument('-p', '--prefix', nargs='*', default=())
parser.add_argument('-s', '--separator', default='__')
# CSV params
parser.add_argument('-d', '--delimiter', default=',')
parser.add_argument('--dialect', default='excel')

args = parser.parse_args()

pprint(dict(flatten(json.loads(args.input.read()), tuple(args.prefix), args.separator)))
