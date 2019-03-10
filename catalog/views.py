from django.shortcuts import render

from .models import Author, Book, BookInstance, Genre
from django.views import generic
# Create your views here.

def index(request):
    """View function for the home page"""

    # Generate the number of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.count()

    context = {
        'num_books': num_authors,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
    }

    return render(request,'index.html', context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    pagination = 10