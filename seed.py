from app import create_app
from models import db, Review, Reply


app = create_app()


sample_reviews = [
("Алексей", 5, "Отличный товар! Превзошёл ожидания."),
("Марина", 4, "Хорошее качество, но доставка заняла больше времени."),
("Иван", 5, "Рекомендую, всё как в описании."),
("Ольга", 3, "Нормально, но есть мелкие недочёты."),
("Сергей", 2, "Не подошёл, не доволен."),
("Екатерина", 5, "Пять звёзд — сервис на высоте."),
("Дмитрий", 4, "Хорошо, куплю ещё."),
("Наталья", 5, "Спасибо! Всё супер."),
("Павел", 4, "Цена-качество ок."),
("Виктория", 5, "Лучшее, что я покупала в этом году.")
]


with app.app_context():
    db.drop_all()
    db.create_all()
    for a, r, c in sample_reviews:
        rev = Review(author=a, rating=r, content=c)
        db.session.add(rev)
    db.session.commit()
    # добавим пару ответов к первому отзыву
    first = Review.query.first()
    if first:
        db.session.add(Reply(review=first, author='Support', content='Спасибо за отзыв!'))
        db.session.commit()
    print('Seed completed')