#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        res_dict = {
            "index": "Welcome to Newsletter RESTful API!"
        }

        return make_response(
            jsonify(res_dict), 200
        )
api.add_resource(Index, '/')


class Newsletters(Resource):
    def get(self):
        data = Newsletter.query.all()

        return make_response(
            jsonify([{
                "id": single_data.id,
                "title": single_data.title,
                "body":single_data.body,
                "published_at": single_data.published_at,
                "edited_at": single_data.edited_at
            } for single_data in data
            
            ]), 200
        )
    
    def post(self):
        new_newsletter = Newsletter(
            title = request.form.get("title"),
            body = request.form.get("body"),
        )

        db.session.add(new_newsletter)
        db.session.commit()

        return make_response(
            jsonify({
                "id": new_newsletter.id,
                "title": new_newsletter.title,
                "body": new_newsletter.body,
                "published_at": new_newsletter.published_at,
                "edited_at": new_newsletter.edited_at
            }), 201
        )
    


api.add_resource(Newsletters, '/newsletters')


class NewsletterById(Resource):

    def get(self, id):
        news_letter = Newsletter.query.filter_by(id=id).first_or_404()

        return make_response(
            jsonify({
                "id": news_letter.id,
                "title": news_letter.title,
                "body": news_letter.body,
                "published_at": news_letter.published_at,
                "edited_at": news_letter.edited_at
            }), 200
        )
    
    def delete(self, id):
        news_letter = Newsletter.query.filter_by(id=id).first()

        db.session.delete(news_letter)
        db.session.commit()

        return make_response(
            jsonify({
                "message": "news letter deleted successfully"
            }), 200
        )

api.add_resource(NewsletterById, "/newsletters/<int:id>")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
