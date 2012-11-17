#!/usr/bin/python2

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

    return output, meta

def parse_file(filename, divider='---'):
    stream = open(filename, 'r').read()
    meta_doc = yaml.load(stream.split(divider)[0])

    if isinstance(meta_doc, str): 
        return { 'body': stream, 'header': None }
    else:
        meta_doc.update({'doc_start': len(meta_doc) + 1 })
        meta_doc.update({'header': True})
        return { 'meta': meta_doc, 'body': stream.split()[1] }

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

        source = parse_document(self.filename, self.data['body'])
        self.document = source[0]
        self.meta = source[1]

        if 'meta' in self.data:
            self.meta.update(self.data['meta'])

    def get_template(self):
        corresponding_template = self.filename_base + '.tmpl'

        if 'meta' in self.data and 'template' in self.data['meta']:
            template = self.data['meta']['template']
        elif os.path.isfile(corresponding_template):
            template = corresponding_template
        else:
            template = DEFAULT_TEMPLATE

        return template

    def output_file(self):
        if 'meta' in self.data and 'output' in self.data['meta']:
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

        with open(self.output_file(), 'w') as f:
            f.write(tmpl)
        
    def dump_metadata(self):
        output = {
            'output': self.output_file(),
            'template': self.get_template(),
            'filename': self.filename
        }

        for k, v in self.meta.iteritems():
            output.update({k: v})

        if 'meta' in self.data:
            output.update(self.data['meta'])
            output.update({'header': True})

        with open(self.filename_base + '.yaml', 'w') as f:
            f.write(yaml.dump(output))

def cli():
    parser = argparse.ArgumentParser(description='Compile a page.')

    parser.add_argument('--builddir', '-b', default="build/", help='Build ouptut directory.')
    parser.add_argument('--metadir', '-m', default="build/meta/", help='Build metadata directory.')
    parser.add_argument('input', nargs='?', help='specify input file.' )
    parser.add_argument('output', nargs='?', default=None, help='specify output file.' )

    return parser.parse_args()

def main():
    interface = cli()

    source = CscPage(interface.input, interface.output, interface.builddir, interface.metadir)
    source.render()
    source.dump_metadata()

    print('[csc] built "' + interface.input + '" into "' + source.output_file() + '"')

if __name__ == '__main__':
    main()
