from django import forms
from .models import Book, Author, Category,Loan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'isbn', 'published_date', 'copies_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'author': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'copies_available': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) != 13 or not isbn.isdigit():
            raise forms.ValidationError("ISBN must be exactly 13 digits and contain only numbers.")
        return isbn

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'biography']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': False}),
        }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }




class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['book', 'loaned_to', 'loaned_date', 'return_date']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'loaned_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter borrower\'s name'}),
            'loaned_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }





from django import forms
from library.models import CustomUser

class CustomSignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        required=True,
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must include at least one digit.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must include at least one letter.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
