from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {
        'name': 'The Cat in the Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]


@app.route('/')
def hello_world():
    return 'Hello World!'
    
#GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})
    
#Define valid book object
def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

#POST /books
@app.route('/books', methods=['POST'])
def add_book():
    #return jsonify(request.get_json())
    request_data = request.get_json()
    if(validBookObject(request_data)):
        books.insert(0, request_data)
        return "True"
    else:
        return "False"
    
@app.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)
    
#app.run(port=5000)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True, port=8000)