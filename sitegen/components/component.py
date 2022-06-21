class Component:
    """Super class for defining components"""

    HTML_TYPES = {'html', 'htm'}

    def __init__(self, file_name='', path=''):
        self.file_name = file_name
        self.path = path

    def load_file(self):
        """Opens and reads in lines from an HTML file in the specified directory."""
        with open(f'{self.path}/{self.file_name}', 'r', newline='') as html_file:
            self.lines = html_file.readlines()

    def __str__(self):
        """Returns all lines in file as string."""
        return ''.join(self.lines)
