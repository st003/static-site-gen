class Component:
    """Base class for defining components"""

    HTML_TYPES: set[str] = {'html', 'htm'}

    def __init__(self, file_name: str ='', path: str =''):
        self.file_name: str = file_name
        self.path: str = path


    def dir_level(self) -> int:
        """
        Returns an integer representing the Component location in a directory
        tree. 0 is the directory root, 1 is a single sub-directory down, etc.
        """
        dirs: list[str] = self.file_name.split('/')
        return len(dirs) - 1


    def get_extention(self) -> str:
        """Returns the file extention."""
        parts: list[str] = self.file_name.split('.')
        extention: int = len(parts) - 1
        return parts[extention]


    def get_name(self) -> str:
        """Returns the file name without file extention."""
        return self.file_name.split('.')[0]


    def load_file(self):
        """Opens and reads in lines from a text file in the specified directory."""
        if self.is_html():
            with open(f'{self.path}/{self.file_name}', 'r', newline='') as text_file:
                self.lines = text_file.readlines()


    def in_sub_dir(self) -> bool:
        """Returns a boolean if the Component resides in a sub-directory."""
        if self.dir_level() > 0:
            return True
        return False


    def is_html(self) -> bool:
        """Returns boolean if project file is html."""
        if self.get_extention() in self.HTML_TYPES:
            return True
        return False


    def __str__(self) -> str:
        """Returns all lines in file as string."""
        return ''.join(self.lines)
