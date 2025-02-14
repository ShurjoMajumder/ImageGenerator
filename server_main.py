from fastapi.responses import FileResponse

from endpoints import basic
from util.server import ServerContext


routers = [
    basic.router,
]

app = ServerContext(*routers)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/cat",

    # Set what the media type will be in the autogenerated OpenAPI specification.
    # fastapi.tiangolo.com/advanced/additional-responses/#additional-media-types-for-the-main-response
    responses={
        200: {
            "content": {"image/png": {}}
        }
    },

    # Prevent FastAPI from adding "application/json" as an additional
    # response media type in the autogenerated OpenAPI specification.
    # https://github.com/tiangolo/fastapi/issues/3258
    response_class=FileResponse
)
async def cat():
    return FileResponse("cat.png", media_type="image/png")
