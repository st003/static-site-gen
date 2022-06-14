import logging
import os

from config import PROJECT_PATH

class ProjectFile:

    HTML_TYPES = {'html', 'htm'}

    def __init__(self, path):
        self.path = path
        self.load_file()
        self.load_layout()
        self.load_blocks()

    def relative_path(self):
        return self.path.removeprefix(f'{PROJECT_PATH}/')

    def get_type(self):
        parts = self.path.split('.')
        extention = len(parts) - 1
        return parts[extention]

    def as_text(self):
        return ''.join(self.lines)

    def uses_layout(self):
        if self.layout_name:
            return True
        return False

    def dir_level(self):
        dirs = self.relative_path().split('/')
        return len(dirs) - 1

    def in_sub_dir(self):
        if self.dir_level() > 0:
            return True
        return False

    def load_file(self):
        with open(self.path, 'r', newline='') as htmlfile:
            self.lines = htmlfile.readlines()

    def load_layout(self):
        if self.lines[0][0:9] == '{% layout':
            self.layout_name = self.lines[0].removeprefix('{% layout ').strip(' %}\n\r')
        else:
            self.layout_name = None

    def load_blocks(self):
        logging.debug(f'loading Blocks for {self}:')
        self.blocks = []

        parsing_block = False
        b = ProjectFile.Block()

        for line in self.lines:

            if not parsing_block:
                if line.strip().startswith('{% block'):
                    parsing_block = True
                    b.name = line.removeprefix('{% block ').strip(' %}\n\r')
            else:
                if line.strip() == '{% endblock %}':
                    b.content = b.content.rstrip('\n\r')
                    self.blocks.append(b)
                    parsing_block = False
                    b = ProjectFile.Block()
                else:
                    b.content += line

        logging.debug(self.blocks)

    def update_relative_paths(self):
        # TODO - what about multiple path tags in a single line?
        for index, line in enumerate(self.lines):
            has_path = line.find('{% path')

            if has_path > -1:
                path_start = has_path + 8
                path_end = line.find(' %}')

                raw_path = line[path_start:path_end]
                path_tag = '{% path ' + raw_path + ' %}'

                for i in range(self.dir_level()):
                    raw_path = f'../{raw_path}'

                rel_path = line.replace(path_tag, raw_path)
                self.lines[index] = rel_path


    def __str__(self):
        return f'ProjectFile(relative_path={self.relative_path()})'

    def __repr__(self):
        return f'ProjectFile(relative_path={self.relative_path()})'

    @classmethod
    def load_project_files(cls, path=PROJECT_PATH):
        project_files = []
        for pf in os.listdir(path):
            if not os.path.isdir(f'{path}/{pf}'):
                project_files.append(ProjectFile(f'{path}/{pf}'))
            else:
                project_files += cls.load_project_files(path=f'{path}/{pf}')
        return project_files


    class Block:

        def __init__(self):
            self.name = None
            self.content = ''

        @property
        def tag_name(self):
            return '{% block ' + self.name + ' %}'

        def __str__(self):
            return f'Block(name={self.name})'

        def __repr__(self):
            return f'Block(name={self.name})'
