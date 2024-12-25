from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, Category, Loan
from .forms import BookForm, AuthorForm, CategoryForm
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from .models import CustomUser
from .forms import CustomSignupForm, CustomLoginForm

from django.core.management import call_command


# Display the list of books with pagination and optional search
@login_required
def book_list(request):
    query = request.GET.get('q', '')  # Search query from the URL
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    
    # Pagination
    paginator = Paginator(books, 10)  # 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'library/book_list.html', {'page_obj': page_obj, 'query': query})

# Add a new book to the library

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # Handles form submissions with file uploads
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to book list after saving the book
    elif request.method == 'GET' and 'generate_fake_books' in request.GET:
        # Trigger the management command to generate fake books
        num_books = int(request.GET.get('num_books', 10))  # Default to 10 books
        call_command('generate_fake_books', num_books=num_books)
        return redirect('book_list')  # Redirect after generating fake books
    else:
        form = BookForm()

    return render(request, 'library/add_book.html', {'form': form})
# Display the list of authors

@login_required
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})

# Add a new author

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'library/add_author.html', {'form': form})

# Display the list of categories

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'library/category_list.html', {'categories': categories})

# Add a new category

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'library/add_category.html', {'form': form})

# Loan a book to a user

@login_required
def loan_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')  # Fetch the selected book ID from the form
        loaned_to = request.POST.get('loaned_to')  # Fetch the borrower's name from the form
        book = get_object_or_404(Book, id=book_id)  # Retrieve the book instance

        if book.copies_available > 0:
            # Create the Loan instance and update book availability
            Loan.objects.create(book=book, loaned_to=loaned_to, loaned_date=now())
            book.copies_available -= 1
            book.save()
            return redirect('loan_list')  # Redirect to the loan list view
        else:
            error = "No copies available for this book."
            books = Book.objects.filter(copies_available__gt=0)
            return render(request, 'library/loan_book.html', {'books': books, 'error': error})
    
    books = Book.objects.filter(copies_available__gt=0)  # Fetch only books with available copies
    return render(request, 'library/loan_book.html', {'books': books})


# Return a book by updating its loan record

@login_required
def return_book(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan = get_object_or_404(Loan, id=loan_id)
        
        if loan.return_date is None:  # Ensure the book hasn't already been returned
            loan.return_date = now()
            loan.book.copies_available += 1
            loan.book.save()
            loan.save()
            return redirect('loan_list')
    
    loans = Loan.objects.filter(return_date__isnull=True)  # Active loans
    return render(request, 'library/return_book.html', {'loans': loans})

# Display a list of all loan recordss

@login_required
def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'library/loan_list.html', {'loans': loans})



def  library_list(request):
    return render(request,'library/library.html')


# views.py


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            CustomUser.objects.create(username=username, password=hashed_password)
            return redirect('login_view')
    else:
        form = CustomSignupForm()
    return render(request, 'library/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.get(username=username)
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('dashboard_view')
                else:
                    form.add_error(None, "Invalid password")
            except CustomUser.DoesNotExist:
                form.add_error(None, "User does not exist")
    else:
        form = CustomLoginForm()
    return render(request, 'library/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def dashboard_view(request):
    total_users = CustomUser.objects.count()
    return render(request, 'library/dashboard.html', {'total_users': total_users})

