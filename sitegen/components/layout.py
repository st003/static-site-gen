"""Contains the Layout class definition."""

from __future__ import annotations

import os
from typing import Optional

from sitegen.config import LAYOUT_EXTENSIONS, LAYOUTS_PATH, log
from sitegen.components.component import Component
from sitegen.components.projectfile import ProjectFile


class Layout(Component):
    """Represents an HTML file to be merged with other project files."""

    def __init__(self, file_name: str, path: str = LAYOUTS_PATH) -> None:
        """Constructs a Layout object instance from file."""
        super().__init__(file_name, path=path)
        self.load_file()


    def compile(self, html_project_file: ProjectFile) -> list[str]:
        """
        Combines a Layout with an HTML project file and returns the updated
        lines in a list.
        """

        pf_blocks: dict[str, ProjectFile.Block] = html_project_file.blocks
        new_lines: list[str] = []

        for line in self.lines:
            found_name: Optional[str] = self.get_block_name_from_line(line)
            # when the line contains a block
            if found_name is not None:
                block: Optional[ProjectFile.Block] = pf_blocks.get(found_name)
                if block is not None:
                    # replace the block tag in the layout with the content of the block
                    line = line.replace(block.tag_name(), block.content)

                else:
                    # when there is no matching block in the ProjectFile
                    # replace the layout block tag with an empty string
                    temp_block: ProjectFile.Block = ProjectFile.Block(found_name)
                    line = line.replace(temp_block.tag_name(), '')

            new_lines.append(line)
        return new_lines


    def __repr__(self) -> str:
        return f'Layout(file_name={self.file_name})'

    @staticmethod
    def get_block_name_from_line(line: str) -> Optional[str]:
        """Search a line for block tag and return the block name if found"""
        # TODO - replace this with a constant defined in a central file
        block_tag_prefix: str = '{% block '
        block_tag_start: int = line.find(block_tag_prefix)

        if block_tag_start > -1:
            name_start_index: int = block_tag_start + len(block_tag_prefix)
            name_end_index: int = line.find(' %}')
            return line[name_start_index:name_end_index]

        return None


    @staticmethod
    def get_all(path: str) -> dict[str, Layout]:
        """
        Returns a dictionary of all Layout files where the key is the layout
        name, and value is the Layout instance.
        """
        log.debug(f'Getting layouts from {path}')

        layouts: dict[str, Layout] = {}
        for html_file in os.listdir(path):

            file_ext: str = html_file.split('.')[-1]
            if file_ext in LAYOUT_EXTENSIONS:
                l: Layout = Layout(html_file, path=path)
                layouts[l.get_name()] = l

        if not len(layouts):
            log.info(f'There are no layouts in {path}')

        return layouts
