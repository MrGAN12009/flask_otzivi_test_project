# Flask Reviews


## Запуск


1. Создайте виртуальное окружение и установите зависимости:


```bash
python -m venv venv
source venv/bin/activate # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```


2. Создайте базу и заполните тестовыми данными:


```bash
python seed.py
```


3. Запустите приложение:


```bash
python app.py
```


Откройте http://127.0.0.1:5000/


## API
- `GET /api/reviews` — список отзывов (включая ответы).
- `POST /api/reviews` — создать отзыв, JSON: `{ "author": "Имя", "rating": 5, "content": "Текст" }`.
- `GET /api/reviews/<id>` — получить отзыв с ответами.
- `POST /api/reviews/<id>/replies` — добавить ответ к отзыву, JSON: `{ "author": "Имя", "content": "Текст ответа" }`.
- `DELETE /api/reviews/<id>` — удалить отзыв (включая ответы).