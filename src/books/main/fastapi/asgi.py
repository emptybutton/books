from books.main.common.asgi import LazyASGIApp
from books.main.fastapi.di import container
from books.presentation.fastapi.app import app_from


app = LazyASGIApp(app_factory=lambda: app_from(container))
