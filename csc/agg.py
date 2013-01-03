#!/usr/bin/python2

# Copyright 2012-2013 Sam Kleinman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Sam Kleinman (tychoish)

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
