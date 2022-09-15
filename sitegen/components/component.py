class Component:
    """Base class for defining components"""

    HTML_TYPES = {'html', 'htm'}

    def __init__(self, file_name='', path=''):
        self.file_name = file_name
        self.path = path


    def dir_level(self):
        """
        Returns an integer representing the Component location in a directory
        tree. 0 is the directory root, 1 is a single sub-directory down, etc.
        """
        dirs = self.file_name.split('/')
        return len(dirs) - 1


    def get_extention(self):
        """Returns the file extention."""
        parts = self.file_name.split('.')
        extention = len(parts) - 1
        return parts[extention]


    def get_name(self):
        """Returns the file name without file extention."""
        return self.file_name.split('.')[0]


    def load_file(self):
        """Opens and reads in lines from a text file in the specified directory."""
        if self.is_html():
            with open(f'{self.path}/{self.file_name}', 'r', newline='') as text_file:
                self.lines = text_file.readlines()


    def in_sub_dir(self):
        """Returns a boolean if the Component resides in a sub-directory."""
        if self.dir_level() > 0:
            return True
        return False


    def is_html(self):
        """Returns boolean if project file is html."""
        if self.get_extention() in self.HTML_TYPES:
            return True
        return False


    def __str__(self):
        """Returns all lines in file as string."""
        return ''.join(self.lines)
