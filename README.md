* установка зависимостей `pip install - r requirements.txt`
* поднять БД в докере (установлен) `docker-compose up -d`
* запустить сервис (FastApi приложение) `uvicorn main:app --reload`
* [сваггер сервиса] (http://127.0.0.1:8008/docs)
* выполнение автотестов на сервис
  - выполнить все `pytest`
  - только смоук `pytest -m smoke`

