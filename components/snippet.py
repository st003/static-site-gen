"""Contains the Snippet class definition."""
import os

from config import SNIPPETS_PATH

class Snippet:
    """Represents a collection of text to be inserted into a project file."""

    def __init__(self, file_name):
        """Constructs a Snippet instance from file."""
        self.file_name = file_name
        self.load_file()

    def tag_name(self):
        """Tag for this Snippet as it would appear in a project file."""
        name = self.file_name.split('.')[0]
        return '{{ ' + name + ' }}'

    def to_string(self):
        """Returns all file lines as a string."""
        return ''.join(self.lines)

    def load_file(self):
        """Opens and reads in lines from an HTML file in the snippets directory."""
        with open(f'{SNIPPETS_PATH}/{self.file_name}', 'r', newline='') as html_file:
            self.lines = html_file.readlines()

    def __str__(self):
        return f'Snippet(file_name={self.file_name})'

    def __repr__(self):
        return f'Snippet(file_name={self.file_name})'

    @staticmethod
    def insert(html_project_file, snippets):
        """Inserts snippets into snippets tags in a project file."""
        lines = html_project_file.lines
        for index, line in enumerate(lines):
            # OPTIMIZE - store blocks in a dict to eliminiate nested loops
            for s in snippets:
                line = line.replace(s.tag_name(), s.to_string())
            lines[index] = line
        return lines

    @staticmethod
    def get_all():
        """Returns a list of all Snippets in the Snippet's directory."""
        snippets = []
        for html_file in os.listdir(SNIPPETS_PATH):
            s = Snippet(html_file)
            snippets.append(s)
        return snippets
