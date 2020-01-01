from django.contrib import admin
from .models import Publisher, Author, Book


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    # List_Filter does Not only works DateField,
    # but also works another DateField
    list_filter = ('publication_date',)
    # The way to show Date Field is
    # using date_hierarchy admin option
    date_hierarchy = 'publication_date'
    # It can Sort or Reverse Publication_Date Data
    ordering = ('-publication_date',)
    # It can hide publication_date Field as Editor Function
    # fields = ('title', 'authors', 'publisher', 'publication_date')
    # fields = ('title', 'authors', 'publisher')
    # User can add new book using incomplete or improperly formed
    # as User set publication_date as None,
    # So you should check fields has null=True or not.

    # It can search the options dynamic and
    # The Writer who chose from writer box can
    # move it other way or move forward.
    # Using Left and Right.
    # --> But, I prefer filter_horizontal
    filter_horizontal = ('authors',)

    # Using Up and Down.
    # filter_vertical = ('authors',)

    # filter_horizontal and filter_vertical
    # are just work on ManyToManyField not ForeignKey Field
    # When use <select>, The Administrator of WebSite don't
    # want that it should select entire date which is relater to
    # View on Drop Down, called OverHead

    # Which means we needs to load all data, publisher,
    # and it will takes time to load Add book.
    # So we use raw_id_fields options.

    # But it just view publisher's ID
    # not publisher name.
    raw_id_fields = ('publisher',)


admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
