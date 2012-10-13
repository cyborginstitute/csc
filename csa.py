#!/usr/bin/python2
"""
Goals:

- Generate an RST page given:

  - a title,
  - a list of pages to inline-include, and
  - a blurb (optional)

- Generate an RST page given:
  - title
  - blurb
  - list of links

Notes:

- Page definitions are yaml files
- a subclass of CscPage(?)

"""

import yaml

def cli():
    import argparse

    parser = argparse.ArgumentParser('build rst page from a yaml spec')
    parser.add_argument('input', nargs='?', help='specify input file.' )

    return parser.parse_args()

def parse_page(input):
    page = open(input, 'r').read()

    parsed = yaml.load(page)

    print parsed


def main():
    interface = cli()

    parse_page(interface.input)

if __name__ == '__main__':
    main()
