import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')  # Replace with your actual project name
import django
django.setup()

# Import necessary models
from library.models import Book, Author, Category  # Replace with your app's name
from faker import Faker
from random import randint

fake = Faker()

def populate_books(n):
    for i in range(n):
        # Generate fake data
        ftitle = fake.sentence(nb_words=5)  # Title of the book
        fauthor_name = fake.name()  # Author name
        fcategory_name = fake.word()  # Category name
        fisbn = fake.isbn13()[:13]  # This ensures that the ISBN is exactly 13 characters long.
  # Generate a valid ISBN-13
        fdate = fake.date_this_decade()  # Publish date
        fcopies_available = randint(1, 100)  # Random number of copies available
        cover_image = None  # Optional (or you can use fake.image_url() if you want to generate URLs)

        # Get or create author and category (avoid duplicates)
        author, created = Author.objects.get_or_create(name=fauthor_name)
        category, created = Category.objects.get_or_create(name=fcategory_name)

        # Create a book record
        Book.objects.get_or_create(
            title=ftitle,
            author=author,
            category=category,
            isbn=fisbn,  # Ensure this is 13 characters long (valid ISBN)
            published_date=fdate,
            copies_available=fcopies_available,
            cover_image=cover_image
        )

    print(f'{n} fake book records inserted successfully!')

# Get number of records from user input
n = int(input('Enter number of records to generate: '))
populate_books(n)
