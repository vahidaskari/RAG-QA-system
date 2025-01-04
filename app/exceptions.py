class GeneralException(Exception):
    def __init__(self, status_code: int = 500, message: str = "Internal server error!"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class InternalServerError(GeneralException):
    def __init__(self):
        super().__init__(
            status_code=500,
            message="Internal server error!",
        )


class TooManyFilesError(GeneralException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message="Maximum number of 5 files is allowed!",
        )


class FileSizeError(GeneralException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message="Files size should not be more than 100 MB!",
        )


class FileTypeError(GeneralException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message="File format not Acceptable, only PDF files are supported!",
        )


class NoContextError(GeneralException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message="No data found from your documents! try diffrent file or question.",
        )


class InvalidDocumentId(GeneralException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message="ID is not valid! it must be a 12-byte input or a 24-character hex string.",
        )
