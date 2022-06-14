"""Contains the Layout class definition."""
import os

from config import LAYOUTS_PATH

class Layout:
    """Represents an HTML file to be merged with other project files."""

    def __init__(self, file_name):
        """Constructs a Layout object instance from file."""
        self.file_name = file_name
        self.load_file()

    def get_name(self):
        """Returns the file name without file extention."""
        return self.file_name.split('.')[0]

    def load_file(self):
        """Opens and reads in lines from an HTML file in the layouts directory."""
        with open(f'{LAYOUTS_PATH}/{self.file_name}', 'r', newline='') as html_file:
            self.lines = html_file.readlines()

    def compile(self, html_project_file):
        """Combines a Layout with an HTML project file and returns a new copy."""
        new_lines = []
        for line in self.lines:
            # OPTIMIZE - store blocks in a dict to eliminiate nested loops
            for b in html_project_file.blocks:
                line = line.replace(b.tag_name(), b.content)
            new_lines.append(line)
        return new_lines

    def __str__(self):
        return f'Layout(file_name={self.file_name})'

    def __repr__(self):
        return f'Layout(file_name={self.file_name})'

    @staticmethod
    def get_all():
        """
        Returns a dictionary of all Layout files where the key is the layout
        name, and value is the Layout instance.
        """
        # TODO - check for invalid file types?
        layouts = {}
        for html_file in os.listdir(LAYOUTS_PATH):
            l = Layout(html_file)
            layouts[l.get_name()] = l
        return layouts
