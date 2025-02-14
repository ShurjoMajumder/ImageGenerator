import pyray as rl

from fastapi import FastAPI, APIRouter


class ServerContext(FastAPI):
    """
    Singleton context manager. Ensures that there is only one active server, and ensures that CLI and FastAPI usage of
    the renderer throw the correct error message if there is an active server or not.
    """

    active_context: 'ServerContext' = None

    def __new__(cls, *_routers):
        """
        This is a singleton class, therefore a new context shouldn't be created if one already exists.
        """
        if cls.active_context is None:
            # create the server context
            cls.active_context = super(ServerContext, cls).__new__(cls)

        return cls.active_context

    def __init__(self, *routers: APIRouter):
        """
        Singleton context manager. Ensures that there is only one active server, and ensures that CLI and FastAPI usage
        of the renderer throw the correct error message if there is an active server or not.

        :param routers: A sequence of `fastapi.APIRouter` routers to add to the application.
        """

        super().__init__()

        # Initialize raylib with hidden window
        rl.set_config_flags(rl.ConfigFlags.FLAG_WINDOW_HIDDEN)
        rl.init_window(0, 0, "test window")

        self.include_routers(*routers)

    def include_routers(self, *routers: APIRouter):
        """
        Adds routers from varargs to the application.

        :param routers: A sequence of `fastapi.APIRouter`.
        """
        for router in routers:
            self.include_router(router)
