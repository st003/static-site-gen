"""Contains the Snippet class definition."""

from __future__ import annotations

import os

from .component import Component
from sitegen.config import SNIPPETS_PATH, log


class Snippet(Component):
    """Represents a collection of text to be inserted into a project file."""

    def __init__(self, file_name: str, path: str = SNIPPETS_PATH) -> None:
        """Constructs a Snippet instance from file."""
        super().__init__(file_name, path=path)
        self.load_file()


    def tag_name(self) -> str:
        """Tag for this Snippet as it would appear in a project file."""
        name: str = self.file_name.split('.')[0]
        return '{{ ' + name + ' }}'


    def __repr__(self) -> str:
        return f'Snippet(file_name={self.file_name})'


    @staticmethod
    def insert(html_project_file, snippets) -> list[str]:
        """Inserts snippets into snippets tags in a project file."""
        lines: list[str] = html_project_file.lines
        for index, line in enumerate(lines):
            # OPTIMIZE - store blocks in a dict to eliminiate nested loops
            for s in snippets:
                line = line.replace(s.tag_name(), str(s))
            lines[index] = line
        return lines


    @staticmethod
    def get_all(path) -> list[Snippet]:
        """Returns a list of all Snippets in the Snippet's directory."""

        log.debug(f'Getting snippets from {path}')

        snippets: list[Snippet] = []
        for html_file in os.listdir(path):
            s: Snippet = Snippet(html_file, path=path)
            snippets.append(s)

        if not len(snippets):
            log.warn(f'There are no snippets in {path}')

        return snippets
