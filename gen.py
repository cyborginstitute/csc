#!/usr/bin/python2

import yaml
from cstools import expand_tree

def filter_inputs(input_list, limit=None, sort=1): 
    if sort is 1: 
        input_list.sort(reverse=False)
    elif sort is -1:
        input_list.sort(reverse=True)

    if limit is None:
        return input_list
    else: 
        return input_list[:limit]

def matcher(input_list, query=None): 
    if query is None:
        return expand_tree(input_list)
    else:
        meta = expand_tree(input_list, 'yaml')
        corpus = {}
        for page in meta: 

            dmeta = yaml.load(open(page, 'r')) 
            if query['key'] in dmeta and dmeta[query['key']] is query['value']: 
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
