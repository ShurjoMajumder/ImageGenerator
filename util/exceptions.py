from colorama import Fore

from util.server import ServerContext
from fastapi.exceptions import HTTPException


class ImgApiException(Exception):
    """
    Exception class for Zephyr things. Works for both the CLI and server, as well as util and renderer libraries.
    """

    def __init__(self, message, error_data: dict):
        super().__init__(message)

        self.error_data = error_data

        self.handle_error()

    def handle_error(self):
        if ServerContext.active_context:
            raise HTTPException(status_code=self.error_data["code"], detail=self.error_data["message"])

        print(Fore.RED + "Oops! Something went wrong!")
        print(Fore.RED + self.error_data["code"])
        print(Fore.RED + self.error_data["message"])
