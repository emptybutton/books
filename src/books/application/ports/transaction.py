from contextlib import AbstractAsyncContextManager
from typing import Any


class SerializabilityError(Exception): ...


type Transaction = AbstractAsyncContextManager[Any]
