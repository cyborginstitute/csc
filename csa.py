#!/usr/bin/python2

import yaml
import argparse

import gen
import agg

########## rendering ##########

def render_title(title):
    line = '=' * len(title)
    return [ line , title , line ]

def render(definition, rendered_content):
    output = render_title(definition['title'])

    for line in [' ', [definition['preamble']] , ' ']:
        output.extend(line)

    output.extend(rendered_content)
    output.append(definition['postamble'])

    return output

def get_output_file(name, input_file):
    if name is None:
        return input_file.rsplit('.', 1)[0] + '.rst'
    else:
        return name

def get_content(pagedef):
    if pagedef['type'] == 'archive': 
        return render(pagedef, agg.render_content(pagedef['pages'], output_type='archive'))
    elif pagedef['type'] == 'generate':
        return gen.render_aggspec(pagedef)
    elif pagedef['type'] == 'directory_archive':
        return agg.directory_archive(pagedef['directory'], output_type='archive')
    elif pagedef['type'] == 'directory_include':
        return agg.directory_archive(pagedef['directory'], output_type='include')

########## interface ##########

class CsaPage(object):
    def __init__(self, inputfile, outputfile):
        self.input = inputfile
        self.input_ext = self.input .rsplit('.', 1)[1]
        self.output = get_output_file(outputfile, self.input)
        self.pagedef = yaml.load_all(open(self.input, 'r').read()).next()
        self.content = get_content(self.pagedef)

    def write(self):
        with open(self.output, 'w') as f: 
            if self.pagedef['type'] == 'archive': 
                for line in self.content: 
                    f.write(line)
                    f.write('\n')
            else: 
                f.write(yaml.dump(self.content))

def cli():
    parser = argparse.ArgumentParser('build rst page from a yaml spec')
    parser.add_argument('input', nargs='?', help='specify input file.' )
    parser.add_argument('output', nargs='?', default=None, help='specify output file.' )
    return parser.parse_args()

def main():
    interface = cli()

    page = CsaPage(interface.input, interface.output)

    page.write()

if __name__ == '__main__':
    main()
