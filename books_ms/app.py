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

class BookModel(db.Model):
    __tablename__="book"
    book_id=db.Column(db.Integer, primary_key=True, nullable=False)
    name=db.Column(db.String(50), nullable=False)
    author=db.Column(db.String(50), nullable=False)
    nr_pages=db.Column(db.Integer, nullable=False)
    description=db.Column(db.String(500), nullable=False)
    price=db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Book(book_id={self.book_id}, name={self.name}, author={self.author}, nr_pages={self.nr_pages}, description={self.description}, price={self.price})"
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
resource_fields={
    'book_id': fields.Integer,
    'name': fields.String,
    'author': fields.String,
    'nr_pages': fields.Integer,
    'description': fields.String,
    'price': fields.Float
}

parser=reqparse.RequestParser()
parser.add_argument('name', type=str, help='Enter the books name')
parser.add_argument('author', type=str, help='Enter the books author')
parser.add_argument('nr_pages', type=int, help='Enter the books nr_pages')
parser.add_argument('description', type=str, help='Enter the books description')
parser.add_argument('price', type=float, help='Enter the books price')

class Books(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return BookModel.get_all()
    
    @marshal_with(resource_fields)
    def post(self):
        args=parser.parse_args(strict=True)
        book=BookModel(
            name=args['name'], 
            author=args['author'],
            nr_pages=args['nr_pages'],
            description=args['description'],
            price=args['price']
            )
        
        db.session.add(book)
        db.session.commit()
        
        return book, 201
    
class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        book=BookModel.get_by_id(book_id)
        return book, 200
    
    @marshal_with(resource_fields)
    def put(self, book_id):
        args=parser.parse_args(strict=True)
        book=BookModel.get_by_id(book_id)
        
        book.name=args['name'], 
        book.author=args['author'],
        book.nr_pages=args['nr_pages'],
        book.description=args['description'],
        book.price=args['price']
        
        db.session.commit()
        
        return book, 204

    def delete(self, book_id):
        book=BookModel.get_by_id(book_id)
        db.session.delete(book)
        db.session.commit()
        
        return '', 204

with app.app_context():
    db.create_all()
    # if (len(sys.argv) > 1 and sys.argv[1]=="create_db"):
        
api.add_resource(Books, '/books')
api.add_resource(Book, '/books/<int:book_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)