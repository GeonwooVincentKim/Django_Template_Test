import csv
import datetime

from django import template
from django.core import mail

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from books.models import Book, Publisher, Author
from books.templatetags.CurrentTimeNode import CurrentTimeNode

from django import template
from django.template import Context, RequestContext, loader
from django.test import TestCase
from django.utils import timezone
from django.views.generic import ListView, DetailView
from reportlab.pdfgen import canvas

register = template.Library()


# Create your views here.
# from django.template import Context


def current_url_view_good(request):
    return HttpResponse("Welcome to the page at %s" % request.path)


def ua_display_good1(request):
    # We cannot believe the data that users Web Browser,
    # and if some unique header are empty or not exist,
    # we should design the application program.
    try:
        ua = request.META['HTTP_USER_AGENT']
    except KeyError:
        return HttpResponse("Your Browser is %s" % ua)


def ua_display_good2(request):
    ua = request.META('HTTP_USER_AGENT', 'unknown')
    return HttpResponse("Your Browser is %s" % ua)


def display_meta(request):
    values = request.META.items()
    # Originally the code was values.sort(),
    # but that code occurs AttributeError()
    # so I changed to sorted(values).
    sorted(values)
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def search_form(request):
    return render(request, 'search_form.html')


# If user visit "/search/" no GET Parameter,
# it appears in the Search form.
def search(request):
    # if 'q' in request.GET and request.GET['q']:
    #     q = request.GET['q']
    #     books = Book.objects.filter(title__icontains=q)
    #     # message = 'You Searched for : %r' % request.GET['q']
    #     return render(request, 'search_results.html',
    #                   {'books': books, 'query': q})
    # else:
    #     # message = 'You Submitted an empty form.'
    #     # return HttpResponse('Please submit a search them.')
    #     # We should follow the procedure starting from
    #     # search_form.html(before click search button)
    #     # so when User click button, it goes to search_result.html
    #     # which shows the result that User inputted.
    #     return render(request, 'search_form.html',
    #                   {'error': True})
    # error = False
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        # If Blanked
        if not q:
            errors.append('Enter a search term.')
        # If over 20 Characters
        elif len(q) > 20:
            errors.append('Please enter at most 20 Characters.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'search_results.html',
                          {'books': books, 'query': q})
    return render(request, 'search_form.html',
                  {'errors': errors})

    # return HttpResponse(message)


def do_current_time(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single"
                                           "argument" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be"
                                           "in quotes" % tag_name)
    return CurrentTimeNode(format_string[1:-1])


def render_(self, context):
    t = context.template.engine_get_template('template_tags.html')
    # new_context = Context({'var': obj}, autoescape=context.autoescape})
    return t.render(Context({'var': context}, autoescape=context.autoescape))


@register.inclusion_tag('books/Templates/template_tags.html', takes_context=True)
def jump_link(context):
    # return render(context, 'template_tags.html', {
    #     'link': context.POST['home_link'],
    #     'title': context.POST['home_title'],
    #     # {'link': 'Hello'}, {'title': 'Hi'}
    # })
    return {
        'link': context['home_link'],
        'title': context['home_title'],
    }


def view_1(request):
    return render(request, 'template1.html',
                  {'message': 'I am view 1.'},
                  context_instance=RequestContext(
                      request, processors=[custom_proc]
                  ))


# All RequestContext includes all variable request which is now
# HttpRequest if this processor activate.
def view_2(request):
    return render(request, 'template2.html',
                  {'message': 'I am View 2.'},
                  context_instance=RequestContext(
                      request, processors=[custom_proc]
                  ))


def custom_proc(request):
    # The Context Processor that provides 'app', 'user' and 'ip_address'
    return {
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }


@register.tag(name="get_current_time")
def current_time_node(request):
    now = datetime.datetime.now()
    return CurrentTimeNode.render(request,
                                  {'get_current_time': now})


@register.inclusion_tag('template_tags.html')
def books_for_author(author):
    books = Book.objects.filter(author)
    # books = Book.objects.filter(author.id)
    return render(author, 'template_tags.html', {'books': books})


register.tag('current_time', do_current_time)


class FormatTimeNode(template.Node):
    def __init__(self, date_to_be_formatted, format_string):
        self.date_to_be_formatted = template.Variable(date_to_be_formatted)
        self.format_string = format_string

    def render(self, context):
        try:
            actual_date = self.date_to_be_formatted.resolve(context)
            return actual_date.strftime(self.format_string)

        except template.VariableDoesNotExist:
            return ''


def do_format_time(parser, token):
    try:
        # split_contests() knows that it doesn't need to
        # identifying A string uniquely.
        tag_name, date_to_be_formatted, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly"
                                           "two arguments" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and
            format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in "
                                           "quotes" % tag_name)
    return FormatTimeNode(date_to_be_formatted, format_string[1:0])


def book_list(request):
    return render(request, 'Templates/template_tags.html', request)


class BookList(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'


class PublisherList(ListView):
    model = Publisher
    context_object_name = 'my_favorite_publishers'


class AcmeBookList(ListView):
    context_object_name = 'book_list'
    queryset = Book.objects.filter(publisher__name='Acme Publishing')
    template_name = 'books/acme_list.html'


class PublisherDetail(DetailView):
    model = Publisher
    context_object_name = 'publisher'
    queryset = Publisher.objects.all()

    def get_context_data(self, **kwargs):
        # Call the basic implementation first and bring Context.
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context


class PublisherBookList(ListView):
    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publishername=self.args[0])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        # Get Context by call Basic implementation.
        context = super(PublisherBookList, self).get_context_data(**kwargs)
        context['publisher'] = self.publisher
        return context


class AuthorDetailView(DetailView):
    queryset = Author.objects.all()

    def get_object(self):
        # Call SuperClass
        object = super(AuthorDetailView, self).get_object()

        # Record the date of last approach.
        object.last_accessed = timezone.now()
        object.save()
        # Return correspondence object
        return object


class EmailTest(TestCase):
    def test_send_email(self):
        # Send Messsage
        mail.send_mail('Subject here', 'Here is the message.',
                       'kdsnop@naver.com', ['kdsnop@daum.net'],
                       fail_sliently=False)

        # Test One Message sent or not
        self.assertEqual(len(mail.outbox), 1)

        # Confirm First Message Subject is correct or not
        self.assertEqual(mail.outbox[0].subject, 'Subject here')


# It automatically save
def some_view(request):
    # Create an HttpResponse object with the appropriate CSV headers.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment;' \
        'filename="somefilename.csv"'

    csv_data = (
        ('First row', 'Foo', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"',
         "Here's a quote"),
    )

    t = loader.get_template('my_template_name.txt')
    c = Context({'data': csv_data, })
    response.write(t.render(c))
    return response
    # writer = csv.writer(response)
    # writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"'])
    # return response


class Echo(object):
    """An object that implements just the write method of the
    file-like interface."""

    def write(self, value):
        """Write the value by returning it, instead of storing
        in a buffer."""
        return value


def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a series of rows.
    # The range is based on the maximum number of rows
    # that most spreadsheet applications can process
    # as a single sheet.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(rows)
                                      for row in rows), content_type="text/csv")
    response['Content-Disposition'] \
        = 'attachment;' \
          'filename="somefilename.csv"'
    return response


def pdf_some_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] \
        = 'attachment;' \
          'filename="somefilename.pdf"'

    # Use the response object as "file"
    # to create the PDF object.
    p = canvas.Canvas(response)

    # Draw a picture on the PDF.
    # This is where the creation of the PDF takes place.
    # See the ReportLab documentation for the full list of features.
    p.drawString(100, 100, "Hello world.")

    # Closing the PDF object ends.
    p.showPage()
    p.save()
    return response
