from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for books
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"}
]

# Routes for CRUD operations

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": books})

# Get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is not None:
        return jsonify({"book": book})
    else:
        return jsonify({"error": "Book not found"}), 404

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    new_book['id'] = len(books) + 1
    books.append(new_book)
    return jsonify({"message": "Book created successfully", "book": new_book})

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is not None:
        updated_book = request.get_json()
        book.update(updated_book)
        return jsonify({"message": "Book updated successfully", "book": book})
    else:
        return jsonify({"error": "Book not found"}), 404

# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({"message": "Book deleted successfully"})

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "message": "Something went wrong on the server"}), 500

if __name__ == '__main__':
    app.run(debug=True)