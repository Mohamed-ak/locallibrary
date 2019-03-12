from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

    # Number of visits to this view
    num_visits = request.session.get("num_visits",1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_authors,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
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


class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to the current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan for librarians"""
    permission_required = 'catalog.can_mark_returned'
    model =  BookInstance
    template_name = 'catalog/bookinstance_list_loan_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
