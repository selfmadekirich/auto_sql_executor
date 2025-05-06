from fastapi import HTTPException


class UnsupportedAIModel(HTTPException):

    def __init__(self):
        self.message = "Provided model is not supported for selected service"
        super().__init__(status_code=404, detail=self.message)
