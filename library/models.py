from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.title


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loaned_to = models.CharField(max_length=255)
    loaned_date = models.DateField(default=now)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.loaned_to} - {self.book.title}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, email=email)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, email=None):
        user = self.create_user(username, password, email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)  # Optional email field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Ensure email is required when creating superuser

    def __str__(self):
        return self.username
