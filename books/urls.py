from books.views import PublisherList, PublisherBookList, AuthorDetailView
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^hi', views.do_current_time, name='current_time'),
    url(r'^view_1/', views.view_1, name='view_1'),
    url(r'^view_2/', views.view_2, name='view_2'),
    url(r'^search-form/', views.search_form),
    url(r'^search/', views.search),
    url(r'^Book_Test/', views.jump_link),
    url(r'^test/', views.current_url_view_good),
    url(r'^displays/', views.ua_display_good2),
    url(r'^display/', views.display_meta),
    # url(r'^publisher/', views.PublisherDetail),
    url(r'^publisher/', PublisherList.as_view(), name='publisher_list'),
    url(r'^books/([\w-]+)/$', PublisherBookList.as_view()),
    url(r'^authors/(?P<pk>[0-9]+)/$', AuthorDetailView.as_view()),
    # url(r'^current/', views.get_current_time, name='get_current_time'),
    # url(r'^current_2/', include('', namespace='current_time')),
    # url(r'^time_node/', )
    # url(r'^time_node/(?P<token>\d+)/', views.do_format_time),
    # url(r'^$', views.book_list)
    url(r'^csv_test/', views.some_view),
    url(r'^csv_test_2/', views.some_streaming_csv_view),
    url(r'^pdf_test/', views.pdf_some_view),
    url(r'^pdf_test_2/', views.pdf_some_view_2),
]
