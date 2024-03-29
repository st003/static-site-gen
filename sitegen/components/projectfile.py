"""Contains the ProjectFile class definition."""

from __future__ import annotations

import os
import shutil
from typing import Optional

import sitegen
from sitegen.components.component import Component
from sitegen.components.constants import TAG_BLOCK_END, TAG_BLOCK_PREFIX, TAG_LAYOUT_PREFIX, TAG_PATH_PREFIX, TAG_SUFFIX
from sitegen.config import log, PROJECT_PATH
from sitegen.exceptions import TagSyntaxError


class ProjectFile(Component):
    """Represents a static file to be evaluted, altered, and exported."""

    def __init__(self, file_name: str, path: str = PROJECT_PATH) -> None:
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


    def load_blocks(self) -> None:
        """Checks for and loads any text blocks."""
        log.debug(f'Loading Blocks for {repr(self)}:')

        self.blocks: dict[str, ProjectFile.Block] = {}
        parsing_block: bool = False
        block: Optional[ProjectFile.Block] = None

        for line in self.lines:

            if not parsing_block:
                if line.strip().startswith(TAG_BLOCK_PREFIX):
                    parsing_block = True
                    name: str = line.removeprefix(TAG_BLOCK_PREFIX).strip(f'{TAG_SUFFIX}\n\r')
                    block = ProjectFile.Block(name)
            else:
                if block is not None:
                    if line.strip() == TAG_BLOCK_END:
                        block.content = block.content.rstrip('\n\r')
                        self.blocks[block.name] = block
                        parsing_block = False
                        block = None
                    else:
                        block.content += line

        log.debug(f'Blocks: {self.blocks}')


    def load_layout(self) -> None:
        """Checks for and loads the layout name."""
        if self.lines[0][0:len(TAG_LAYOUT_PREFIX)] == TAG_LAYOUT_PREFIX:
            self.layout_name: str = self.lines[0].removeprefix(TAG_LAYOUT_PREFIX).strip(f'{TAG_SUFFIX}\n\r')
        else:
            self.layout_name = ''


    def save_file(self) -> None:
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


    def update_relative_paths(self) -> None:
        """Checks for any path tags and updates paths to be relative."""
        log.debug(f'Updating paths for {repr(self)}')

        for index, line in enumerate(self.lines):

            current_line: str = line
            check_for_paths: bool = True

            while check_for_paths:

                tag_start: int = current_line.find(TAG_PATH_PREFIX)

                # -1 is the return value of find() when substring is not found
                if tag_start > -1:

                    # raw path should begin 8 chars after the tag start
                    path_start: int = tag_start + 8
                    path_end: int = current_line.find(TAG_SUFFIX)

                    # when missing closing bracket
                    if path_end == -1:
                        # generate preview at least 50 chars of raw path. Str slice already handles out of bounds exceptions
                        tag_preview: str = current_line[tag_start:(tag_start + 8 + 50)]
                        raise TagSyntaxError(f'closing bracket for path tag missing in file: {self.file_name} at:\n\n{tag_preview}...\n')

                    raw_path: str = current_line[path_start:path_end]
                    path_tag: str = TAG_PATH_PREFIX + raw_path + TAG_SUFFIX
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
    def load_project_files(cls, base_path: str, sub_path: str = '') -> list[ProjectFile]:
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

        def __init__(self, name: str) -> None:
            self.name: str = name
            self.content: str = ''

        def tag_name(self) -> str:
            """The tag name as it would appear for this Block."""
            return TAG_BLOCK_PREFIX + self.name + TAG_SUFFIX

        def __str__(self) -> str:
            return self.content

        def __repr__(self) -> str:
            return f'Block(name={self.name})'
