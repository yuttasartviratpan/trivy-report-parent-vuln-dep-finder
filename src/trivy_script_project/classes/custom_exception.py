class FileExtensionNotSupported(Exception):
    def __init__(self, file_extension, message=None):
        """Initialize the custom exception with a message and an error code."""
        self.file_extension = file_extension
        self.message = message

    def __str__(self):
        """Return a string representation of the exception."""
        if self.message is not None:
            return f"{self.message} "

        if self.file_extension is None:
            return "File extension was not provided, please provide a file extension"
        else:
            return f"File extension of type {self.file_extension} was not supported"

    @classmethod
    def edit_error_message(cls, message):
        return cls(message)

