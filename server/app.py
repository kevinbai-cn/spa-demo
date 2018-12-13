# coding=utf-8

from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort


app = Flask(__name__)
api = Api(app)


books = [{'id': 1, 'name': 'book1', 'category': 'cat1'},
         {'id': 2, 'name': 'book2', 'category': 'cat2'},
         {'id': 3, 'name': 'book3', 'category': 'cat3'}]


def get_by_id(book_id):
    book = [v for v in books if v['id'] == book_id]
    return book[0] if book else None


def get_or_abort(book_id):
    book = get_by_id(book_id)
    if not book:
        abort(404, message=f'Book {book_id} not found')
    return book


def not_empty_str(s):
    s = str(s)
    if not s:
        raise ValueError("Must not be empty string")
    return s


class BookApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=not_empty_str, required=True, location='json')
        self.reqparse.add_argument('category', type=not_empty_str, required=True, location='json')
        super(BookApi, self).__init__()
        
    def get(self, book_id):
        book = get_or_abort(book_id)
        return book

    def put(self, book_id):
        book = get_or_abort(book_id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            book[k] = v
        return book, 201

    def delete(self, book_id):
        book = get_or_abort(book_id)
        del book
        return '', 204


class BookListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=not_empty_str, required=True, location='json')
        self.reqparse.add_argument('category', type=not_empty_str, required=True, location='json')
        super(BookListApi, self).__init__()

    def get(self):
        return books

    def post(self):
        args = self.reqparse.parse_args()
        book = {
            'id': books[-1]['id'] + 1 if books else 1,
            'name': args['name'],
            'category': args['category'],
        }
        books.append(book)
        return book, 201


api.add_resource(BookApi, '/api/v1/books/<int:book_id>', endpoint='book')
api.add_resource(BookListApi, '/api/v1/books', endpoint='books')

if __name__ == '__main__':
    app.run(debug=True)
