from books.main.common.uvicorn import run_dev


def main() -> None:
    run_dev("books.main.fastapi.asgi:app")


if __name__ == "__main__":
    main()
