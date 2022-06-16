"""Contains the ProjectFile class definition."""
import logging
import os

from sitegen.config import PROJECT_PATH

class ProjectFile:
    """Represents a static file to be evaluted, altered, and exported."""

    HTML_TYPES = {'html', 'htm'}

    def __init__(self, path):
        """
        Constructs a ProjectFile instance from a file path and configures any
        Layouts and Blocks.
        """
        self.path = path
        self.load_file()
        self.load_layout()
        self.load_blocks()

    def relative_path(self):
        """Returns the relative path for this file from the project root."""
        return self.path.removeprefix(f'{PROJECT_PATH}/')

    def get_extention(self):
        """Returns the file extention."""
        parts = self.path.split('.')
        extention = len(parts) - 1
        return parts[extention]

    def to_string(self):
        """Returns all text lines into a single string."""
        return ''.join(self.lines)

    def extends_layout(self):
        """Returns a boolean indicating if this ProjectFile extends a layout."""
        if self.layout_name:
            return True
        return False

    def dir_level(self):
        """
        Returns an integer representing the ProjectFile location in a directory
        tree. 0 is the directory root, 1 is a single sub-directory down, etc.
        """
        dirs = self.relative_path().split('/')
        return len(dirs) - 1

    def in_sub_dir(self):
        """Returns a boolean if the ProjectFile resides in a sub-directory."""
        if self.dir_level() > 0:
            return True
        return False

    def load_file(self):
        """Opens and reads in lines from the ProjectFile's path."""
        with open(self.path, 'r', newline='') as htmlfile:
            self.lines = htmlfile.readlines()

    def load_layout(self):
        """Checks for and loads the layout name."""
        if self.lines[0][0:9] == '{% layout':
            self.layout_name = self.lines[0].removeprefix('{% layout ').strip(' %}\n\r')
        else:
            self.layout_name = None

    def load_blocks(self):
        """Checks for and loads any text blocks."""
        logging.debug(f'loading Blocks for {self}:')
        self.blocks = []

        parsing_block = False
        b = ProjectFile.Block()

        for line in self.lines:

            if not parsing_block:
                if line.strip().startswith('{% block'):
                    parsing_block = True
                    b.name = line.removeprefix('{% block ').strip(' %}\n\r')
            else:
                if line.strip() == '{% endblock %}':
                    b.content = b.content.rstrip('\n\r')
                    self.blocks.append(b)
                    parsing_block = False
                    b = ProjectFile.Block()
                else:
                    b.content += line

        logging.debug(self.blocks)

    def update_relative_paths(self):
        """Checks for any path tags and updates paths to be relative."""
        # TODO - what about multiple path tags in a single line?
        for index, line in enumerate(self.lines):
            has_path = line.find('{% path')

            if has_path > -1:
                path_start = has_path + 8
                path_end = line.find(' %}')

                raw_path = line[path_start:path_end]
                path_tag = '{% path ' + raw_path + ' %}'

                for i in range(self.dir_level()):
                    raw_path = f'../{raw_path}'

                rel_path = line.replace(path_tag, raw_path)
                self.lines[index] = rel_path


    def __str__(self):
        return f'ProjectFile(relative_path={self.relative_path()})'

    def __repr__(self):
        return f'ProjectFile(relative_path={self.relative_path()})'

    @classmethod
    def load_project_files(cls, path=PROJECT_PATH):
        """
        Scans all directories and sub-directories in the project path, loads
        each file into a ProjectFile instance and returns the collection as
        a list.
        """
        project_files = []
        for pf in os.listdir(path):
            if not os.path.isdir(f'{path}/{pf}'):
                project_files.append(ProjectFile(f'{path}/{pf}'))
            else:
                project_files += cls.load_project_files(path=f'{path}/{pf}')
        return project_files


    class Block:
        """A section of a ProjectFile to be loaded into a layout."""

        def __init__(self):
            self.name = None
            self.content = ''

        def tag_name(self):
            """The tag name as it would appear for this Block."""
            return '{% block ' + self.name + ' %}'

        def __str__(self):
            return f'Block(name={self.name})'

        def __repr__(self):
            return f'Block(name={self.name})'
