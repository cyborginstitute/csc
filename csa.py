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
import argparse

def cli():
    parser = argparse.ArgumentParser('build rst page from a yaml spec')
    parser.add_argument('input', nargs='?', help='specify input file.' )
    parser.add_argument('output', nargs='?', default=None, help='specify output file.' )

    return parser.parse_args()

def parse_page(input):
    page = open(input, 'r').read()
    return yaml.load_all(page).next()

def render_title(title):
    output = []

    lines = '=' * len(title)
    output.append(lines)
    output.append(title)
    output.append(lines)
    output.append('')

    return output

def render_includes(pages):
    output = []

    for page in pages:
        output.append('.. include:: ' + page)
        meta = yaml.load(open(page.rsplit('.', 1)[0] + '.yaml', 'r').read())
        if 'header' in meta:
            output.append('   :start-line: ' + str(meta['doc_start']))
        output.append('')

    return output

def render_archive(pages):
    output = []

    for page in pages:
        meta = yaml.load(open(page.rsplit('.', 1)[0] + '.yaml', 'r').read())
        output.append('- `' + meta['title'] + ' </' + meta['output'] + '>' + '`_')

    output.append('')

    return output

def render(definition):
    output = []
    output.extend(render_title(definition['title']))

    output.append(definition['preamble'])
    output.append('')

    if definition['type'] == 'include':
        output.extend(render_includes(definition['pages']))
    elif definition['type'] == 'archive':
        output.extend(render_archive(definition['pages']))

    output.append(definition['postamble'])

    return output

def main():
    interface = cli()

    if interface.output is None:
        output_file = interface.input.rsplit('.', 1)[0] + '.rst'
    else:
        output_file = interface.output

    output = open(output_file, 'w')

    for line in render(parse_page(interface.input)):
        output.write(line)
        output.write('\n')

if __name__ == '__main__':
    main()
