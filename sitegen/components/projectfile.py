"""Contains the ProjectFile class definition."""

import os
import shutil

from .component import Component
from sitegen.config import log, DIST_PATH, PROJECT_PATH


class ProjectFile(Component):
    """Represents a static file to be evaluted, altered, and exported."""

    def __init__(self, file_name, path=PROJECT_PATH):
        """
        Constructs a ProjectFile instance from a file path and configures any
        Layouts and Blocks.
        """
        super().__init__(file_name=file_name, path=path)
        log.debug(f'Loading {repr(self)}')
        self.load_file()

        if self.is_html():
            self.load_layout()
            self.load_blocks()


    def extends_layout(self):
        """Returns a boolean indicating if this ProjectFile extends a layout."""
        if self.layout_name:
            return True
        return False


    def load_blocks(self):
        """Checks for and loads any text blocks."""
        log.debug(f'Loading Blocks for {repr(self)}:')
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

        log.debug(f'Blocks: {self.blocks}')


    def load_layout(self):
        """Checks for and loads the layout name."""
        if self.lines[0][0:9] == '{% layout':
            self.layout_name = self.lines[0].removeprefix('{% layout ').strip(' %}\n\r')
        else:
            self.layout_name = None


    def save_file(self):
        """Saves file to specificed location."""

        # create sub-directory if needed
        if (self.in_sub_dir()):
            sub_dir = f'{DIST_PATH}/{os.path.dirname(self.file_name)}'
            os.makedirs(sub_dir, exist_ok=True)

        if self.is_html():
            log.debug(f'Exporting {repr(self)}')
            with open(f'{DIST_PATH}/{self.file_name}', 'w', newline='') as outfile:
                outfile.writelines(self.lines)
        else:
            log.debug(f'Copying {repr(self)}')
            shutil.copyfile(f'{PROJECT_PATH}/{self.file_name}', f'{DIST_PATH}/{self.file_name}')


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


    def __repr__(self):
        return f'ProjectFile(file_name={self.file_name})'


    @classmethod
    def load_project_files(cls, base_path=PROJECT_PATH, sub_path=''):
        """
        Scans all directories and sub-directories in the project path, loads
        each file into a ProjectFile instance and returns the collection as
        a list.
        """
        project_files = []

        full_path = base_path if not sub_path else f'{base_path}/{sub_path}'
        for proj_file in os.listdir(full_path):

            if not os.path.isdir(f'{full_path}/{proj_file}'):
                # prepend the sub_path of present
                proj_file_name = proj_file if not sub_path else f'{sub_path}/{proj_file}'
                project_files.append(ProjectFile(proj_file_name, path=base_path))
            else:
                # recursively run the method when a sub-directory is found
                new_sub_path = proj_file if not sub_path else f'{sub_path}/{proj_file}'
                project_files += cls.load_project_files(base_path=base_path, sub_path=new_sub_path)

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
            return self.content


        def __repr__(self):
            return f'Block(name={self.name})'
