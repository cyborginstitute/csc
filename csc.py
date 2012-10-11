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
import sys

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
    stream = open(filename, 'r').read().split(divider, 2)
    meta = None

    for segment in stream:
        try:
            meta = yaml.load(segment)
        except ( yaml.scanner.ScannerError, SyntaxError ):
            body = segment

    return {'meta': meta, 'body': body }

class CscPage(object):
    def __init__(self, input_file, output_file):
        self.filename = input_file
        self.output_arg = output_file
        self.data = parse_file(self.filename)
        self.filename_base = ''.join(self.filename.split('.', -1)[:-1])
        self.document = parse_document(self.filename, self.data['body'], self.data['meta'])
        self.template = self.get_template()
        self.output = self.get_output()

    def get_template(self):
        corresponding_template = self.filename_base + '.tmpl'

        if 'template' in self.data['meta']:
            template = self.data['meta']['template']
        if os.path.isfile(corresponding_template):
            template = corresponding_template
        else:
            template = 'detail.tmpl'

        return template

    def get_output(self):
        if 'output' in self.data:
            output = self.data['meta']['output']
        elif self.output_arg is not None:
            output = self.output_arg
        else:
            output = self.filename_base + '.html'

        return output

    def render(self):
        options = {}

        env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'), **options)
        tmpl = env.get_template(self.template).render(entry=self.document).encode('UTF-8')

        output = open(self.output, 'w')
        output.write(tmpl)
        output.close()

    def dump_metadata(self):
        f = open(self.filename_base + '.yaml', 'w')

        output = {
            'output': self.output,
            'template': self.template,
            'filename': self.filename
        }

        output.update(self.data['meta'])

        f.write(yaml.dump(output))
        f.close

def csc_cmd_line_interface():
    num_args = len(sys.argv)

    if num_args > 3:
        exit("Too many arguments.")
    elif num_args is 0:
        exit("Not enough arguments.")
    elif num_args is 1:
        input_file = sys.argv[1]
        output_file = None
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    return input_file, output_file

def main():
    input_file, output_file = csc_cmd_line_interface()
    source = CscPage(input_file, output_file)

    source.render()
    source.dump_metadata()

if __name__ == '__main__':
    main()
