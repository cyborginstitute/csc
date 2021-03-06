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

def filter_inputs(input_list, limit=None, sort=1):
    if limit is None or limit >= len(input_list):
        if sort == 1:
            return input_list.sort(reverse=False)
        elif sort == -1:
            return input_list.sort(reverse=True)
    elif limit == 1: 
        if sort is 1:
            return input_list.min()
        elif sort is -1:
            return input_list.max()
    else:
        import heapq
        if sort is 1: 
            return heapq.nsmallest(limit, input_list)
        elif sort is -1:
            return heapq.nlargest(limit, input_list)

def matcher(input_list, query=None):
    if query is None:
        return expand_tree(input_list)
    else:
        meta = expand_tree(input_list, 'yaml')
        corpus = {}
        for page in meta:
            dmeta = yaml.load(open(page, 'r'))
            if query['key'] in dmeta and (
                    (dmeta[query['key']] is query['value']) or
                    (query['value'] in dmeta[query['key']])):
                pass
            else:
                corpus[page.rsplit('.')[0] + '.rst'] = dmeta

    return corpus.keys()

def render_aggspec(spec):
    filtered_list = matcher(spec['input'], spec['filter'])

    pages = filter_inputs(filtered_list, spec['limit'], spec['sort'])

    agg_spec = {
        'title':spec['title'],
        'type': spec['final_type'],
        'preamble': spec['preamble'],
        'postamble': spec['postamble'],
        'pages': pages
    }

    return agg_spec

if __name__ == '__main__':
    pass
