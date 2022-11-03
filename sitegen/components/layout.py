"""Contains the Layout class definition."""

from __future__ import annotations

import os

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

        new_lines: list[str] = []
        for line in self.lines:
            for block in html_project_file.blocks:
                line = line.replace(block.tag_name(), block.content)
            new_lines.append(line)
        return new_lines


    def __repr__(self) -> str:
        return f'Layout(file_name={self.file_name})'


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
            log.warn(f'There are no layouts in {path}')

        return layouts
