from flask import Flask, jsonify, request, Response
import json

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
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Try a valid format? =)"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
    
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
    

#PUT
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()

   #if(not valid_put_request_data(request_data)):
   #    invalidBookObjectErrorMsg = {
   #        "error": "Valid book must be passed in the request",
   #        "helpstring": "Require name and price. ISBN is the URL"
   #    }
   #    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
   #    return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }

    # Verify if the isbn/book exists
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i+=1
        response = Response("", status=204)
        return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    update_book = {}
    if("name" in request_data):
        update_book["name"] = request_data['name']
    if("price" in request_data):
        update_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(update_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

if __name__ == '__main__':
    #app.run(host="0.0.0.0", debug = True, port=8000)
    app.run(host="127.0.0.1", debug = True, port=8000)