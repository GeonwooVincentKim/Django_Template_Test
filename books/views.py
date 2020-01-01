import datetime

from django import template

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from books.models import Book
from books.templatetags.CurrentTimeNode import CurrentTimeNode

from django import template
from django.template import Context, RequestContext

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
    if not(format_string[0] == format_string[-1] and format_string[0] in ('"',"'")):
        raise template.TemplateSyntaxError("%r tag's argument should be"
                                           "in quotes" % tag_name)
    return CurrentTimeNode(format_string[1:-1])


def render_(self, context):
    t = context.template.engine_get_template('template_tags.html')
    # new_context = Context({'var': obj}, autoescape=context.autoescape})
    return t.render(Context({'var': context}, autoescape=context.autoescape))


@register.inclusion_tag('template_tags.html', takes_context=True)
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


@register.inclusion_tag('template_tags.html')
def books_for_author(author):
    books = Book.objects.filter(author)
    # books = Book.objects.filter(author.id)
    return render(author, 'template_tags.html', {'books': books})


@register.assignment_tag
def get_current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


register.tag('current_time', do_current_time)
