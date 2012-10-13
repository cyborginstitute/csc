#!/usr/bin/python2
"""
TODO:

  - Refactor csc_cmnd_line_interface() to be argparsy
  - add support for specifiable build directory.
  - add support for putting yaml files and html files seperate
  - make it possible to dump doctrees
"""

from docutils.core import publish_parts
import jinja2
import yaml
import os.path
import argparse

DEFAULT_TEMPLATE = 'detail.tmpl'
DEFAULT_BUILDDIR = 'build/'

def render_rst(filename, input):
    output = {}
    overrides = {'doctitle_xform': True,
                 'initial_header_level': 1}
    rst_output = publish_parts(
                        source=input,
                        settings_overrides=overrides,
                        writer_name='html',
                        enable_exit_status=True)

    content = [ rst_output['html_title'], rst_output['html_subtitle'], rst_output['body'] ]

    output['file'] = filename
    output['content'] = ''.join(content)
    output['title'] = rst_output['title']
    output['subtitle'] = rst_output['html_subtitle']

    return output

def parse_document(filename, input, meta=None):
    output = {}

    if meta is None:
        meta = {}
    else:
        for key in meta:
            output[key] = meta[key]

    rst_output = render_rst(filename, input)

    meta.setdefault('title', rst_output['title'])
    meta.setdefault('name', rst_output['title'])

    if len(rst_output['subtitle']) is not 0:
        meta.setdefault('subtitle', rst_output['subtitle'])

    output['content'] = rst_output['content']

    return output

def parse_file(filename, divider='---'):
    stream = open(filename, 'r').read()
    split_stream = stream.split(divider, 2)

    if split_stream[0] == '':
        return { 'meta': yaml.load(split_stream[1]), 'body': split_stream[2] }
    else:
        return { 'meta': None, 'body': stream }

class CscPage(object):
    def __init__(self, input_file, output_file, build_arg=None, meta_arg=None):
        self.arg = {
            'filename': input_file,
            'output': output_file,
            'builddir': build_arg,
            'meta': meta_arg,
            }

        self.filename = self.arg['filename']
        self.filename_base = ''.join(self.filename.split('.', -1)[:-1])
        self.data = parse_file(self.filename)
        self.document = parse_document(self.filename, self.data['body'], self.data['meta'])

    def get_template(self):
        corresponding_template = self.filename_base + '.tmpl'

        if self.data['meta'] is not None and 'template' in self.data['meta']: 
            template = self.data['meta']['template']
        elif os.path.isfile(corresponding_template):
            template = corresponding_template
        else: 
            template = DEFAULT_TEMPLATE
            
        return template

    def output_file(self):
        if self.data['meta'] is not None and 'output' in self.data['meta']:
            r = self.data['meta']['output']
        elif self.arg['output'] is not None:
            r = self.arg['output']
        else:
            r = self.filename_base + '.htm'

        return r

    def get_builddir(self):
        if 'buildir' in self.data['meta']:
            r = self.data['meta']['builddir']
        elif self.arg['builddir'] is not None:
            r = self.arg['builddir']
        else:
            r = DEFAULT_BUILDDIR

        return r

    def render(self):
        options = {}

        env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'), **options)
        tmpl = env.get_template(self.get_template()).render(entry=self.document).encode('UTF-8')

        output = open(self.output_file(), 'w')
        output.write(tmpl)
        output.close()

    def dump_metadata(self):
        f = open(self.filename_base + '.yaml', 'w')

        output = {
            'output': self.output_file(),
            'template': self.get_template(),
            'filename': self.filename
        }

        if self.data['meta'] is None: 
            output = self.data['meta']
        else: 
            output.update(self.data['meta'])

        f.write(yaml.dump(output))
        f.close

def csc_cmd_line_interface():
    parser = argparse.ArgumentParser(description='Compile a page.')

    parser.add_argument('--builddir', '-b', default="build/", help='Build ouptut directory.')
    parser.add_argument('--metadir', '-m', default="build/meta/", help='Build metadata directory.')
    parser.add_argument('input', nargs='?', help='specify input file.' )
    parser.add_argument('output', nargs='?', default=None, help='specify output output.' )

    return parser.parse_args()

def main():
    interface = csc_cmd_line_interface()

    source = CscPage(interface.input, interface.output, interface.builddir, interface.metadir)
    source.render()
    source.dump_metadata()

    print('[csc] built "' + interface.input + '" into "' + source.output_file() + '"')

if __name__ == '__main__':
    main()
  
