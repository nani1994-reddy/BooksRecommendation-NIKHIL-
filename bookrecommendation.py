import json
import os

# File path to store book data and user ratings
BOOK_FILE = r"C:\miracle intern\Book Recommendation System\books.json"  # Use a valid JSON file path for storing data

# Ensure the directory exists or create it
os.makedirs(os.path.dirname(BOOK_FILE), exist_ok=True)

# Function to load data from the JSON file
def load_data():
    if os.path.exists(BOOK_FILE):  # Check if the file exists
        with open(BOOK_FILE, 'r') as file:
            return json.load(file)  # Return the data in the file
    return {"books": [], "ratings": {}}  # Return empty data if file doesn't exist

# Function to save data to the JSON file
def save_data(data):
    with open(BOOK_FILE, 'w') as file:  # Open the file for writing
        json.dump(data, file, indent=4)  # Write the data to the file

class TrieNode:
    def __init__(self):
        self.children = {}   # Dictionary to store child nodes
        self.is_end_of_word = False  # Marks if the node represents the end of a word

class Trie:
    def __init__(self):
        self.root = TrieNode()  # Root of the trie

    def insert(self, title):
        node = self.root  # Start at the root node
        for char in title.lower():
            if char not in node.children:
                node.children[char] = TrieNode()  # Create a new node if character not found
            node = node.children[char]  # Move to the next node
        node.is_end_of_word = True  # Mark the end of a word

    def search(self, prefix):
        node = self.root  # Start at the root
        for char in prefix.lower():  # Traverse the trie using the prefix
            if char not in node.children:
                return []  # Prefix not found
            node = node.children[char]  # Move to the next node
        return self._collect_all_titles(node, prefix)  # Collect all titles with the prefix

    def _collect_all_titles(self, node, prefix):
        results = []
        if node.is_end_of_word:
            results.append(prefix)
        for char, child_node in node.children.items():
            results.extend(self._collect_all_titles(child_node, prefix + char))
        return results

class BookRecommendationSystem:
    def __init__(self):
        self.data = load_data()  # Load book and rating data from JSON
        self.trie = Trie()  # Initialize Trie
        self.load_books_into_trie()  # Insert all books into trie

    def load_books_into_trie(self):
        for book in self.data['books']:
            self.trie.insert(book['title'])  # Insert all book titles into the trie

    def add_book(self, title, author, genre):
        book = {"title": title, "author": author, "genre": genre}
        self.data['books'].append(book)
        self.trie.insert(title)  # Insert book title into trie
        save_data(self.data)  # Save updated data
        print(f"Book '{title}' added successfully.")

    def view_books(self):
        if not self.data['books']:
            print("No books available.")
        else:
            for i, book in enumerate(self.data['books'], start=1):
                print(f"{i}. Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")

    def rate_book(self, username, book_title, rating):
        if username not in self.data['ratings']:
            self.data['ratings'][username] = {}
        self.data['ratings'][username][book_title] = rating
        save_data(self.data)
        print(f"Rating for '{book_title}' saved successfully.")

    def get_recommendations(self, username):
        if username not in self.data['ratings']:
            print("No ratings found for user.")
            return
        rated_books = self.data['ratings'][username].keys()
        genres = [book['genre'] for book in self.data['books'] if book['title'] in rated_books]
        recommended_books = [book for book in self.data['books'] if book['genre'] in genres and book['title'] not in rated_books]
        if not recommended_books:
            print("No recommendations available.")
        else:
            for book in recommended_books:
                print(f"Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")

    def search_books(self, prefix):
        search_results = self.trie.search(prefix)
        if not search_results:
            print("No books found with that prefix.")
        else:
            for title in search_results:
                book = next((b for b in self.data['books'] if b['title'].lower() == title.lower()), None)
                if book:
                    print(f"Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")

# Main application loop
def main():
    app = BookRecommendationSystem()  # Initialize the system

    while True:
        print("\nOptions:")
        print("1. Add Book")
        print("2. View Books")
        print("3. Rate Book")
        print("4. Get Recommendations")
        print("5. Search Books")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':  # Add Book
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            genre = input("Enter book genre: ")
            app.add_book(title, author, genre)

        elif choice == '2':  # View Books
            app.view_books()

        elif choice == '3':  # Rate Book
            username = input("Enter your username: ")
            app.view_books()
            book_number = int(input("Select a book number to rate: ")) - 1
            if 0 <= book_number < len(app.data['books']):
                rating = int(input("Enter your rating (1-5): "))
                book_title = app.data['books'][book_number]['title']
                app.rate_book(username, book_title, rating)
            else:
                print("Invalid book number.")

        elif choice == '4':  # Get Recommendations
            username = input("Enter your username: ")
            app.get_recommendations(username)

        elif choice == '5':  # Search Books
            prefix = input("Enter book title prefix to search: ")
            app.search_books(prefix)

        elif choice == '6':  # Exit
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
