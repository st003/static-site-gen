import os

from config import LAYOUTS_PATH

class Layout:

    def __init__(self, file_name):
        self.file_name = file_name
        self.load_file()

    @property
    def name(self):
        return self.file_name.split('.')[0]

    def load_file(self):
        with open(f'{LAYOUTS_PATH}/{self.file_name}', 'r', newline='') as htmlfile:
            self.lines = htmlfile.readlines()

    def compile(self, html_file):
        new_lines = []
        for line in self.lines:
             # INVESTIGATE - It might be more optimized to check each
            # line for any tags before calling compile
            for b in html_file.blocks:
                line = line.replace(b.tag_name, b.content)
            new_lines.append(line)
        return new_lines

    def __str__(self):
        return f'Layout(file_name={self.file_name})'

    def __repr__(self):
        return f'Layout(file_name={self.file_name})'

    @staticmethod
    def get_all():
        layouts = {}
        for html_file in os.listdir(LAYOUTS_PATH):
            l = Layout(html_file)
            layouts[l.name] = l
        return layouts
