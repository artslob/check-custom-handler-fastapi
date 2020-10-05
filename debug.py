#!/usr/bin/env python


def main():
    import uvicorn

    app = "check_handler.asgi:app"
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", reload=True)


if __name__ == "__main__":
    main()
