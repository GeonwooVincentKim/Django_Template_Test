from books.models import Book
from django import template

from django.http import *
from django.template import Template, Context, loader, RequestContext
import datetime

from django.template.loader import get_template

from .forms import ContactForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from django.conf import settings

t = get_template('book_snippet.html')
register = template.Library()


def current_datetime(request):
    # Set time UTC(UTF) time to UTF-8 automatically
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html',
                  {'current_date': now})
    # dt = datetime.datetime.now() + datetime.timedelta(hours=offset)

    # fp = open('/home/django_user/Templates/mytemplate.html')
    # t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    # t = get_template('current_datetime.html')
    # t2 = Template("This is # comment")
    # fp.close()
    # html = t.render(Context({'current_date': now}))
    # html = "<html><body>It is now %s</body></html>" % now
    # return HttpResponse(html)
    # t = get_template('Templates/current_datetime.html')
    # html = t.render(Context({'current_date': now}))
    # return HttpResponse(html)

    # return render(request, 'current_datetime.html',
    #               {'hour_offset': offset}, {'next_time': dt})


def future_datetime(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s. </body></html>" % (offset, dt)
    return HttpResponse(html)
    # return render(request, 'future_datetime.html',
    #               {''})
    # now = datetime.datetime.now()
    # dt = now + datetime.timedelta(hours=offset)
    # return render(request, 'future_datetime.html',
    #               {'hour_offset': now, 'next_time': dt})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                # cd.get('email',
                # ['noreply@example.com](mailto:'noreply%40@example.com)'),
                # [['siteowner@example.com](mailto:'siteowner%40example.com)'],
                cd.get('email', ['noreply@example.com']),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(
            # =initial={'subject': 'I love your site!'}
        )
    return render(request, 'contact_form.html', {'form': form})


def debug(request):
    DEBUG = True


# View (in reviews / views.py)
def page(request, num="1"):
    # Prints the corresponding web page of the review item according to num.
    print("Mumbling")


# def redirect_to_year(request):
#     year = 2012
#     return HttpResponseRedirect(reverse('reviews-year-archive'
#                                         args=(year,)))


# def view_1(request):
#     t = loader.get_template('template1.html')
#     c = Context({
#         'app': 'My app',
#         'user': request.user,
#         'ip_address': request.META['REMOTE_ADDR'],
#         'message': 'I am view 1.'
#     })
#     return t.render(c)


# def view_2(request):
#     t = loader.get_template('template2.html')
#     c = Context({
#         'app': 'My app',
#         'user': request.user,
#         'ip_address': request.META['REMOTE_ADDR'],
#         'message': 'I am the second view.'
#     })
#     return t.render(c)

# All RequestContext includes all variable request which is now
# HttpRequest if this processor activate.
# def view_2(request):
#     return render(request, 'template2.html',
#                   {'message': 'I am View 2.'},
#                   context_instance=RequestContext(
#                       request, processors=[custom_proc]
#                   ))

# Register is also django.template.Library instance
# as before
# @register.inclusion_tag('book_snippet.html')
# def show_reviews(review):
#     books = Book.objects.filter(authors__id=author.id)
#     return {'books': books}
#
#
# register.inclusion_tag(t)(show_reviews)
#
#
# @register.inclusion_tag('link.html', takes_context=True)
# def jump_link(context):
#     return {
#         'link': context['home_link'],
#         'title': context['home_title'],
#     }
#
