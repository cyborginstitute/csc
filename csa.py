#!/usr/bin/python2

import yaml
import argparse
import os
import sys

DEFAULT_EXTENSION = 'rst'

def render_title(title):
    line = '=' * len(title)
    return [ line , title , line ]

def render_content(pages, output_type='archive'):
    output = []

    if output_type = 'archive': 

        for page in pages:
            meta = parse_meta(page)
            output.append('- `' + meta['title'] + ' </' + meta['output'] + '>' + '`_')

        output.append('')

    elif output_type = 'includes': 

        for page in pages:
            output.append('.. include:: ' + page)
            meta = parse_meta(page)

            if 'header' in meta:
                output.append('   :start-line: ' + str(meta['doc_start']))

            output.append('')

    return output

def render_directory_archive(directory, output_type='archive', input_extension=DEFAULT_EXTENSION):
    file_list = []

    for root, subFolders, files in os.walk(directory):
        for file in files:
            f = os.path.join(root,file)

            if f.rsplit('.', 1)[1] == input_extension:
                file_list.append(f)

    if output_type == 'archive':
        return render_archive(file_list)
    elif output_type == 'include':
        return render_includes(file_list)
    else:
        return None

def render(definition):
    output = render_title(definition['title'])

    for line in [' ', [definition['preamble']] , ' ']:
        output.extend(line)

    if definition['type'] == 'directory_archive':
        output.extend(render_directory_archive(definition['directory'], output_type='archive'))
    elif definition['type'] == 'directory_include':
        output.extend(render_directory_archive(definition['directory'], output_type='include'))
    else: 
        output.extend(render_content(definition['pages'], definition['type']))

    output.append(definition['postamble'])

    return output

def write_file(output_file, content):
    output = open(output_file, 'w')

    for line in content:
        output.write(line)
        output.write('\n')

    output.close()

def get_output_file(name, input_file):
    if name is None:
        return input_file.rsplit('.', 1)[0] + '.rst'
    else:
        return name

def parse_page(input):
    return yaml.load_all(open(input, 'r').read()).next()

def parse_meta(input_page, yaml_extension='yaml'):
    return yaml.load(open(input_page.rsplit('.', 1)[0] + '.' + yaml_extension, 'r').read())

def cli():
    parser = argparse.ArgumentParser('build rst page from a yaml spec')
    parser.add_argument('input', nargs='?', help='specify input file.' )
    parser.add_argument('output', nargs='?', default=None, help='specify output file.' )

    return parser.parse_args()

def main():
    interface = cli()

    write_file( output_file=get_output_file(interface.output, interface.input),
                content=render(parse_page(interface.input)) )

if __name__ == '__main__':
    main()
