# uvicorn app:app
gunicorn 'user_service.__main__:get_app()'