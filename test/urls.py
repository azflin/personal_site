from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test_function/$', views.test_function, name='test_function'),
    url(r'^test_poll/$', views.test_poll, name='test_poll')
]