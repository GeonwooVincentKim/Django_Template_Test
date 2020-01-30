"""Main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from books.views import PublisherList
from django.conf.urls import include, url
from django.contrib import admin
# from django.views.debug import *
# from My_Django_Template_1_2.Main.views import current_datetime
# from django.urls import path, include

# from . import views
from .views import current_datetime
from .views import future_datetime

# from reviews.templatetags.review_extras import *

"""
    Django output procedure
    urls.py -> views.py -> html files(Templates)
"""
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # path('', include())
    # url(r'^time/', current_datetime),

    # TemplateView.as_view(template_name='file_name.html') is
    # just simply render the template files which is in "template_name"

    # url(r'^time/$', TemplateView.as_view(template_name='current_datetime.html')),
    # url(r'^current_datetime/')
    url(r'^time/$', current_datetime),
    # url(r'^reviews/', include('inner'), {}),
    url(r'^time/plus/(d{1,2})/$', future_datetime),
    # url(r'^future_time/plus/(\d+)/$', future_datetime)
    # url(r'^future_time', )

    url(r'^books/', include('books.urls')),
    # url(r'^books/', include('books.urls', namespace='books')),
    # url(r'^books/$', include('books.urls', namespace='books')),
    # url(r'^books/$', include('books.urls', namespace='books')),
    # url(r'^test_1/', include('test_1.urls', namespace='test_1')),
    # url(r'^contact/$', include('django_website.contact.urls')),
    # url(r'^community/', include('django_website.aggregator.urls')),
    # url(r'^articles/2003/$', views.special_case_2003),
    # url(r'^reviews/([0-9]{4})/$', views.year_archive,
    #     name='reviews-year-archive'),
    # url(r'^view_1/', view_1),
    # url(r'^view_2/', view_2),
    # url(r'^Inclusion/', jump_link),
    # url(r'^testtest/', current_time),
    # url(r'^')
    # url(r'^$', views.homepage),
    # url(r'^(\d{4})/([a-z]{3})/$', views.archive_month),

]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
# import debug_toolbar
# urlpatterns += [
#     url(r'^__debug__/', include(debug_toolbar.urls)),
# ]

# if settings.DEBUG:
#     urlpatterns += [url(r'^debuginfo/$', views.debug), ]
