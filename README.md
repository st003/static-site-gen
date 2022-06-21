# Static Site Generator

A Jinja-inspired Python program for compiling static web files. User defined layouts and snippets allow for dynamically inserting text into HTML pages. Example uses include inserting redundant markup like navigation, CSS, and JavaScript into multiple pages.

### Prerequisites

Python 3.8+

### Installing

Download a copy of the repository and extract to your file system. A simple example project site can be found in the examples directory.

### Usage

To start, create a new project folder by running:

```
python -m sitegen --new
```

Place all of your project files and directories in the project/source folder. See the docs for detailed instructions on how to dynamically insert text into project files.

When you are ready to generate your site, run:

```
python -m sitegen
```

The final output will be saved to the dist folder. A full list of optional arguments can be viewed by running:

```
python -m sitegen --help
```

## Running the tests

From the program root directory, run:

```
python -m unittest discover tests
```

## Built With

* [Python](https://www.python.org/) - Language interpreter
