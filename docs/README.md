# Static Site Generator - Manual

A Jinja-inspired Python program for compiling static web files. User defined layouts and snippets allow for dynamically inserting text into HTML pages. Example uses include inserting redundant markup like navigation, CSS, and JavaScript into multiple pages.

## Project Structure

Sites are generated from a folder in the root directory call project. Within this folder are three sub-folders: source, layouts, snippets.

A new project folder can be created by running the command:

```
python -m sitegen --new
```

### Source

The pages to be compiled into a static site. Arbitrary sub-directory structure is supported and maintained during output. Only files with the extension: .html and .htm will be modified.

### Layouts

Layouts are used to define common page structures to be used on one or more pages. Example use-cases include: inserting CSS, JavaScript, and other HTML head content, or page navigation, headers, footers, etc.

To specify when to use a layout in a page, use the tag:

```
{% layout <name> %}
```

in the first line of the page, where name is the name of the layout file without the file extension. The layout tag must be used in the first line of the page, else the layout will not be used.

A layout file is a simple HTML file located in the layouts folder. Within a layout file, special tags define where text is merged from the page.

#### Blocks

A block is a section of page text to be merged into the layout at a specific location. For example, in a layout with a common navigation element, this could be the content section that is unique to each page.

In the layout file, a block is specified with the tag:

```
{% block <name> %}
```

Where name is the user defined name of the block. During site generation, the page content to be merged into a layout's block tag(s) is pulled from the text wrapped by a similarly named block start and end tag:

```
{% block <name> %}
Hello, World!
{% endblock %}
```

There are no limits to the number of blocks a layout may have.

#### Paths

Paths are used to ensure links maintain the correct relative path regardless of folder hierarchy. When defining a URL in a page, layout, or snippet for another file in the project, always use the tag:

```
{% path <url> %}
```

where url is the full path to the file location from the project source root. During site generation, path tags will be updated with the correct relative paths, either up or down the folder hierarchy. Do not use the path tag for external urls.

### Snippets

Snippets are re-usable text components to be inserted directly into a layout or page. Snippet files are stored in the snippets folder and are specified in a layout or page with the tag:

```
{{ <name> }}
```

where name is the name of the snippet file without the file extension.

## Generating Your Site

To generate your final output, run the command:

```
python -m sitegen
```

The program will merge your pages with any applicable layouts, set relative paths, and insert any snippets. By default, the final output will be saved to the dist folder in your root directory. However, you can set a custom output directory with the --dist flag:

```
python -m sitegen --dist=/path/to/output
```

## Example

An example project is included in the examples folder and can be generated for output using the command:

```
python -m sitegen --example
```
