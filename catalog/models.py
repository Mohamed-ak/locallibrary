from django.db import models

# to get the absolute url for a detail record
from django.urls import reverse 

# required for unique book instances
import uuid


class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200, help_text = "Enter a book genre (e.g. Science Fiction")

    def __str__(self):
        """String representing the Genre object."""
        return self.name

class Book(models.Model):
    """Model representing a book(not a specific copy of a book)."""
    title = models.CharField(max_length=200, help_text="Enter a title of the book")
    # author as a string because the model author has not been defined yet
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String representing the Book object"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book"""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Model representing an instance of a book"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique Id for this particular book across the whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m',"Maintenance"),
        ('o',"On loan"),
        ('a',"Available"),
        ('r',"Reserved"),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m',help_text="Book availability")

    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        """String representing the BookInstance object"""
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Author object."""
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """Model representing a language in which a book may be written"""
    name = models.CharField(max_length=200, help_text="Enter the name of the language")

    def __str__(self):
        """String representing a Language object"""
        return self.name