"""Custom exceptions."""

class ProjectHierarchyError(Exception):
    """Exception for when there are issues with the project folder."""
    pass

class TagSyntaxError(Exception):
    """Exception for when the user has a syntax error with a tag."""
    pass
