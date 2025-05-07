from fastapi import HTTPException


class UnknownAIProfile(HTTPException):

    def __init__(self):
        self.message = "Got unknown AI profile id"
        super().__init__(status_code=404, detail=self.message)


class DatabaseUnreachable(HTTPException):

    def __init__(self):
        self.message = "Unable to reach remote database host!"
        super().__init__(status_code=404, detail=self.message)


class GenerationError(HTTPException):

    def __init__(self, reason=""):
        self.message = f"Unable to generate query due to {reason}"
        super().__init__(status_code=404, detail=self.message)
