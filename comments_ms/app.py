from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, reqparse
import sys
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:admin@database/books_ms'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SQLALCHEMY_ECHO']=True

api=Api(app)
db=SQLAlchemy(app)

class CommentModel(db.Model):
    __tablename__="comment"
    comment_id=db.Column(db.Integer, primary_key=True, nullable=False)
    comment=db.Column(db.String(255), nullable=False)
    first_name=db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    rate=db.Column(db.Integer, nullable=False)
    book_id=db.Column(db.Integer, nullable=False)
    
    @classmethod
    def get_all_by_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id).first()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
        
        
resource_fields={
    'comment_id': fields.Integer,
    'comment': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'rate': fields.Float,
    'book_id': fields.Integer
}

parser=reqparse.RequestParser()
parser.add_argument('comment', type=str, help='Enter the books name')
parser.add_argument('first_name', type=str, help='Enter the books author')
parser.add_argument('last_name', type=str, help='Enter the books nr_pages')
parser.add_argument('rate', type=float, help='Enter the book rate')
parser.add_argument('book_id', type=int, help='Enter the book id')

class BookComments(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        return CommentModel.get_all_by_id(book_id)
    
    @marshal_with(resource_fields)
    def post(self, book_id):
        args=parser.parse_args(strict=True)
        comment=CommentModel(
            comment=args['comment'], 
            first_name=args['first_name'],
            last_name=args['last_name'],
            rate=args['rate'],
            book_id=book_id
            )
        
        db.session.add(comment)
        db.session.commit()
        
        return comment, 201
    
class Comments(Resource):
    @marshal_with(resource_fields)
    def get(self, comment_id):
        comment=CommentModel.get_by_id(comment_id)
        
        return comment, 200
    
    @marshal_with(resource_fields)
    def delete(self, comment_id):
        comment=CommentModel.get_by_id(comment_id)
        db.session.delete(comment)
        db.session.commit()
        
        return '', 204
    
    # @marshal_with(resource_fields)
    # def put(self, book_id):
    #     args=parser.parse_args(strict=True)
    #     book=BookModel.get_by_id(book_id)
        
    #     book.name=args['name'], 
    #     book.author=args['author'],
    #     book.nr_pages=args['nr_pages'],
    #     book.description=args['description'],
    #     book.price=args['price']
        
    #     db.session.commit()
        
    #     return book, 204

with app.app_context():
    db.create_all()

api.add_resource(BookComments, '/bookcomments/<int:book_id>')
api.add_resource(Comments, '/comments/<int:comment_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)