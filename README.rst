===============================
Cyborg Site Generator (``csc``)
===============================

Overview
--------

``csc`` provides a system to generate websites, written with a
combination of reStructuredText marked-up content and YAML specified
composite pages. The goal of this project is to build a system with
the following goals and emphases:

- support efficient builds for large sites, and effective publishing
  workflows that make updating a single page or set of pages as easy
  as rebuilding the full site.

- a system for incremental and multi-core builds is more important
  than a system for fast full-builds.

- Use and reuse existing and proven tools as much as possible.

To develop a solution that supports these goals, ``csc`` consists of
two main components: a page rendering component that takes
reStructuredText files and renders them to HTML using Jinja templates
and a compiled page aggregator component that takes YAML page
definitions and generates reStructuredText that the rendering
component can use to render a page. Each file, including restructured
text content files may have YAML metadata that stores configuration
metadata. To build a ``csc`` site you must render each page, but since
each page embeds its own configuration and metadata, there are minimal
dependencies between pages. You can automate the build process using a
tool like GNU Make or Ninja, which provides reliable and consistent
multi-processing.

Use
---

Operations
~~~~~~~~~~

Clone the ``csc`` repository (e.g. ``git clone
git://github.com/cyborginstitute/csc.git``) and copy the ``csc/``
directory and the ``makefile`` directory into a project directory.

.. note::

   For most deployments, you will commit the ``csc`` code into your own
   project's repository and use ``csc`` *embedded* in your project.

The first section of the ``makefile`` contains user configuration, as
in the following: ::

   ############################################################
   #
   # User configuraiton values.

   PYTHONBIN = python
   source-dir = test
   build-dir = build
   bin-dir = csc

Set the variables as follows:

- ``PYTHONBIN`` - replace with the name of the Python binary that you
  want to use. You may choose to use ``pypy`` or Python 2.7.

- ``source-dir`` - the location of the content source files.

- ``build-dir`` - the location where ``csc`` will write the build
  output of the site

- ``bin-dir`` - the location of the embeded ``csc`` directory with the
  Python scripts.

.. important:: Do not specify paths with trailing slashes.

Content
~~~~~~~

For most pages, will be plain unadorned reStructuredText pages with a
``.rst`` or ``.txt`` extension. You may optionally add a number of
YAML fields and values as a header to these rST pages as
metadata. ``csc`` passes the metadata from the header section to the
template directly. The following meta values are special and read from
the files:

- ``template`` the name and path of the template file that ``csc``
  will use to render the page.

- ``output`` the name of the file that ``csc`` will write the output
  file. If not specified ``csc`` will use the current file name and
  path (with the ``.html`` extension.) This option is typically not
  specified.

- ``builddir`` the path of the output file. This option is typically
  not specified.

Consider the following example of an aggregated page:

**directory.agg**: ::

   type: directory_archive
   preamble: this is the preamble
   postamble: this is the post-amble. lol.
   title: an aggregated page, created
   directory: test/

This will generate a file named ``directory.html``, that contains a
list (i.e. ``archive``) of all the files in the ``test/``
directory. Specify the directory in the ``test/`` relative to the top
level of the source directory, and the corresponding links will be
similarly relative to the top level of the output directory.

You may also specify ``directory_include`` which will create a
restructured text page with ``include::`` directives. When rendered,
the resulting page will have the content of all files in the
directory.

**curate.agg**: ::

   title: 'this is a title'
   type: archive
   archive:
     - input.rst
     - shell-line-eding.rst
   preamble: "this is a bit of text and I think that its important to have text before the list."
   postamble: "this is text and it goes after the end of things."

In this example, rather than including all pages in a directory, you
can specify a list of files and generate either an a list of pages as
above (i.e. ``archive``) or an included page (i.e. ``include``.)

**generated.spec**: ::

   type: generate
   title: this is a generated page
   preamble: this is the preamble
   postamble: this is the post-amble. lol.
   input: test/
   filter:
      tag: 'people'
   sort: 1
   limit: 5
   final_type: archive

The ``generate`` page type creates an aggregated page with some sort
of constraint. You may understand the process for generating a page
using a very simple pipeline: pass the name of a directory in the
``input`` value the contents of tat the pipeline considers. The filter
is a simple field/value pair that all documents must satisfy. The
``sort`` value determines if ``csa`` includes source files by ordered
in ascending (``-1``) or descending (``1``) order. Finally, the
``limit`` defines how many aggregated items ``csa`` includes.

Generated pages may be either listings (i.e. ``archive``) or composite
pages (i.e. ``include``.)

Templates
~~~~~~~~~

``csc`` passes all values specified in the metadata n a page to the
template as variables. Users are responsible for ensuring that
templates only use specified variables. See the documentation of Jinja
for more information.

Internals
---------

The makefile defines and controls basic use and ensures that:

- ``csa.Pu`` processes files with ``.agg`` and ``.spec`` extensions.
  Separate python modules (i.e. ``agg.py`` and ``gen.py``) handle
  processing of the aggregated content depending on the value of the
  ``type`` field in the aggregation definition.

- ``csc.py`` processes files with ``.txt`` and ``.rst`` extension, and
  pass the meta information into from the source file as variables to
  the template.

- the ``makefile`` processes all aggregated pages before all rendered
  pages. Presumably, aggregated pages take more time to process than
  rendered pages.

The ``csc`` Python module contains two primary files:

1. ``csc.py`` which the makefile calls directly to render
   reStructuredText pages into HTML (with Jinja templates.)

2. ``csa.py``, which renders YAML aggregation specifications into
   reStructuredText. Aggregation processing occurs in two subsidiary
   modules: ``agg.py`` and ``gen.py``.

Future Development
------------------

- Better tracking of dependencies of aggregated pages. ``csa.py``
  needs to output ``.d`` files listing dependencies. Conversely, it
  may make sense to have ``csc`` generate a makefile directly with
  more explicit per-file build instructions may result in a more
  simple ``csc`` system, and help improve the initial build
  experience and performance.

- Providing better aggregated page generation and specification. This
  should probably be more plug-able.

- Tests. For everything.

- The rendering classes need to be a little more reliant and
  tested. To this end I'd like to eventually move `tychoish.com
  <http://tychoish.com/>`_ to put ``csc`` through its paces.
