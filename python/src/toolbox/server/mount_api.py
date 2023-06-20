from fastapi import FastAPI


def mount_api(app: FastAPI):
    @app.get("/api")
    def read_root():
        return {"Hello": "World"}

    @app.get("/api/items/{item_id}")
    def read_item(item_id: int, q: str = ""):
        return {"item_id": item_id, "q": q}

    return app
