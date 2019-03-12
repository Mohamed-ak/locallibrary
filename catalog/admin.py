from django.contrib import admin
from .models import Genre, Author, Book, BookInstance, Language
# Register your models here.

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookInline(admin.StackedInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','date_of_birth','date_of_death')
    fields = ['first_name','last_name',('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book','status','borrower','due_back','imprint','id')

    fieldsets = (
        ('Book Information',{
            'fields': ('id','book','imprint')
        }),
        (
            'Availability',{
                'fields':('status','due_back','borrower')
            }
        )
    )
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

