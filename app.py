from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from config import Config
from models import db, Review, Reply
from forms import ReviewForm, ReplyForm


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)


    with app.app_context():
        db.create_all()


    @app.route('/')
    def product_page():
        form = ReviewForm()
        reply_form = ReplyForm()
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        return render_template('product.html', reviews=reviews, form=form, reply_form=reply_form)


    # Site: add review (POST form)
    @app.route('/add-review', methods=['POST'])
    def add_review():
        form = ReviewForm()
        if form.validate_on_submit():
            r = Review(author=form.author.data, rating=form.rating.data, content=form.content.data)
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('product_page'))
        # if validation fails, show product page with errors
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        reply_form = ReplyForm()
        return render_template('product.html', reviews=reviews, form=form, reply_form=reply_form)

    # Site: add reply (POST form)
    @app.route('/reviews/<int:review_id>/reply', methods=['POST'])
    def add_reply(review_id):
        form = ReplyForm()
        review = Review.query.get_or_404(review_id)
        if form.validate_on_submit():
            rp = Reply(review=review, author=form.author.data, content=form.content.data)
            db.session.add(rp)
            db.session.commit()
            return redirect(url_for('product_page') + '#review-' + str(review_id))
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        review_form = ReviewForm()
        return render_template('product.html', reviews=reviews, form=review_form, reply_form=form)

    # API: create review


    @app.route('/api/reviews', methods=['POST'])
    def api_create_review():
        data = request.get_json() or {}
        author = data.get('author')
        rating = data.get('rating')
        content = data.get('content')
        if not author or not content or not isinstance(rating, int) or not (1 <= rating <= 5):
            return jsonify({'error': 'invalid payload'}), 400
        r = Review(author=author, rating=rating, content=content)
        db.session.add(r)
        db.session.commit()
        return jsonify(r.to_dict()), 201

    # API: get review
    @app.route('/api/reviews/<int:review_id>', methods=['GET'])
    def api_get_review(review_id):
        r = Review.query.get_or_404(review_id)
        return jsonify(r.to_dict())

    # API: reply to review
    @app.route('/api/reviews/<int:review_id>/replies', methods=['POST'])
    def api_reply_review(review_id):
        r = Review.query.get_or_404(review_id)
        data = request.get_json() or {}
        author = data.get('author')
        content = data.get('content')
        if not author or not content:
            return jsonify({'error': 'invalid payload'}), 400
        rp = Reply(review=r, author=author, content=content)
        db.session.add(rp)
        db.session.commit()
        return jsonify(rp.to_dict()), 201

    # API: delete review
    @app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
    def api_delete_review(review_id):
        r = Review.query.get_or_404(review_id)
        db.session.delete(r)
        db.session.commit()
        return jsonify({'status': 'deleted'})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)