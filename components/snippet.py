import os

from config import SNIPPETS_PATH

class Snippet:

    def __init__(self, file_name):
        self.file_name = file_name
        self.load_file()

    @property
    def tag_name(self):
        name = self.file_name.split('.')[0]
        return '{{ ' + name + ' }}'

    def load_file(self):
        with open(f'{SNIPPETS_PATH}/{self.file_name}', 'r', newline='') as htmlfile:
            self.text = ''.join(htmlfile.readlines())

    def __str__(self):
        return f'Snippet(file_name={self.file_name})'

    def __repr__(self):
        return f'Snippet(file_name={self.file_name})'

    @staticmethod
    def insert(lines, snippets):
        for index, line in enumerate(lines):
            # INVESTIGATE - It might be more optimized to check each
            # line for any tags before calling insert
            for s in snippets:
                line = line.replace(s.tag_name, s.text)
            lines[index] = line
        return lines

    @staticmethod
    def get_all():
        snippets = []
        for html_file in os.listdir(SNIPPETS_PATH):
            s = Snippet(html_file)
            snippets.append(s)
        return snippets
