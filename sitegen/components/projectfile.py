"""Contains the ProjectFile class definition."""

import os
import shutil

import sitegen
from .component import Component
from sitegen.config import log, PROJECT_PATH
from sitegen.exceptions import TagSyntaxError


class ProjectFile(Component):
    """Represents a static file to be evaluted, altered, and exported."""

    def __init__(self, file_name: str, path: str = PROJECT_PATH):
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


    def extends_layout(self) -> bool:
        """Returns a boolean indicating if this ProjectFile extends a layout."""
        if self.layout_name:
            return True
        return False


    def load_blocks(self):
        """Checks for and loads any text blocks."""
        log.debug(f'Loading Blocks for {repr(self)}:')
        self.blocks: list[ProjectFile.Block] = []

        parsing_block: bool = False
        b: ProjectFile.Block = ProjectFile.Block()

        for line in self.lines:

            if not parsing_block:
                if line.strip().startswith('{% block'):
                    parsing_block: bool = True
                    b.name: str = line.removeprefix('{% block ').strip(' %}\n\r')
            else:
                if line.strip() == '{% endblock %}':
                    b.content: str = b.content.rstrip('\n\r')
                    self.blocks.append(b)
                    parsing_block: bool = False
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
            sub_dir: str = f'{sitegen.DIST_PATH}/{os.path.dirname(self.file_name)}'
            os.makedirs(sub_dir, exist_ok=True)

        if self.is_html():
            log.debug(f'Exporting {repr(self)}')
            with open(f'{sitegen.DIST_PATH}/{self.file_name}', 'w', newline='') as outfile:
                outfile.writelines(self.lines)
        else:
            log.debug(f'Copying {repr(self)}')
            shutil.copyfile(f'{self.path}/{self.file_name}', f'{sitegen.DIST_PATH}/{self.file_name}')


    def update_relative_paths(self):
        """Checks for any path tags and updates paths to be relative."""
        log.debug(f'Updating paths for {repr(self)}')

        for index, line in enumerate(self.lines):

            current_line: str = line
            check_for_paths: bool = True

            while check_for_paths:

                tag_start: int = current_line.find('{% path')

                # -1 is the return value of find() when substring is not found
                if tag_start > -1:

                    # raw path should begin 8 chars after the tag start
                    path_start: int = tag_start + 8
                    path_end: int = current_line.find(' %}')

                    # when missing closing bracket
                    if path_end == -1:
                        # generate preview at least 50 chars of raw path. Str slice already handles out of bounds exceptions
                        tag_preview: str = current_line[tag_start:(tag_start + 8 + 50)]
                        raise TagSyntaxError(f'closing bracket for path tag missing in file: {self.file_name} at:\n\n{tag_preview}...\n')

                    raw_path: str = current_line[path_start:path_end]
                    path_tag: str = '{% path ' + raw_path + ' %}'
                    log.debug(f'found path tag: {path_tag}')

                    for i in range(self.dir_level()):
                        raw_path = f'../{raw_path}'

                    log.debug(f'Updating path tag: {path_tag}')
                    current_line = current_line.replace(path_tag, raw_path)

                else:
                    check_for_paths = False

            self.lines[index] = current_line


    def __repr__(self) -> str:
        return f'ProjectFile(file_name={self.file_name})'


    @classmethod
    def load_project_files(cls, base_path: str, sub_path: str = '') -> list:
        """
        Scans all directories and sub-directories in the project path, loads
        each file into a ProjectFile instance and returns the collection as
        a list.
        """
        project_files: list[ProjectFile] = []

        full_path: str = base_path if not sub_path else f'{base_path}/{sub_path}'
        for proj_file in os.listdir(full_path):

            if not os.path.isdir(f'{full_path}/{proj_file}'):
                # prepend the sub_path of present
                proj_file_name: str = proj_file if not sub_path else f'{sub_path}/{proj_file}'
                project_files.append(ProjectFile(proj_file_name, path=base_path))
            else:
                # recursively run the method when a sub-directory is found
                new_sub_path: str = proj_file if not sub_path else f'{sub_path}/{proj_file}'
                project_files += cls.load_project_files(base_path=base_path, sub_path=new_sub_path)

        return project_files


    class Block:
        """A section of a ProjectFile to be loaded into a layout."""

        def __init__(self):
            self.name = None
            self.content: str = ''

        def tag_name(self) -> str:
            """The tag name as it would appear for this Block."""
            return '{% block ' + self.name + ' %}'

        def __str__(self) -> str:
            return self.content

        def __repr__(self) -> str:
            return f'Block(name={self.name})'
