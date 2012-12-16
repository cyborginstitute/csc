#!/usr/bin/python2

import yaml
from cstools import expand_tree

def parse_meta(input_page, yaml_extension='yaml'):
    return yaml.load(open(input_page.rsplit('.', 1)[0] + '.' + yaml_extension, 'r').read())

def directory_archive(directory, output_type='archive'):
    file_list = expand_tree(directory)
    
    if output_type == 'archive':
        return render_content(file_list, output_type='archive')
    elif output_type == 'include':
        return render_content(file_list, output_type='include')
    else:
        return None

def render_content(pages, output_type='archive'):
    output = []

    if output_type == 'archive': 
        for page in pages:
            meta = parse_meta(page)
            output.append('- `' + meta['title'] + ' </' + meta['output'] + '>' + '`_')

        output.append('')

    elif output_type == 'include': 
        for page in pages:
            output.append('.. include:: ' + page)
            meta = parse_meta(page)

            if 'header' in meta:
                output.append('   :start-line: ' + str(meta['doc_start']))

            output.append('')

    return output

if __name__ == '__main__':
    pass
