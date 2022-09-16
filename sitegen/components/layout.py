"""Contains the Layout class definition."""

from __future__ import annotations

import os

from .component import Component
from sitegen.config import LAYOUTS_PATH, log


class Layout(Component):
    """Represents an HTML file to be merged with other project files."""

    def __init__(self, file_name: str, path: str = LAYOUTS_PATH) -> None:
        """Constructs a Layout object instance from file."""
        super().__init__(file_name, path=path)
        self.load_file()


    def compile(self, html_project_file) -> list[str]:
        """Combines a Layout with an HTML project file and returns a new copy."""
        new_lines: list[str] = []
        for line in self.lines:
            # OPTIMIZE - store blocks in a dict to eliminate nested loops
            for b in html_project_file.blocks:
                line = line.replace(b.tag_name(), b.content)
            new_lines.append(line)
        return new_lines


    def __repr__(self) -> str:
        return f'Layout(file_name={self.file_name})'


    @staticmethod
    def get_all(path) -> dict[str, Layout]:
        """
        Returns a dictionary of all Layout files where the key is the layout
        name, and value is the Layout instance.
        """
        log.debug(f'Getting layouts from {path}')

        # TODO - check for invalid file types?
        layouts: dict[str, Layout] = {}
        for html_file in os.listdir(path):
            l: Layout = Layout(html_file, path=path)
            layouts[l.get_name()] = l

        if not len(layouts):
            log.warn(f'There are no layouts in {path}')

        return layouts
