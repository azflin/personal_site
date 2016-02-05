from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^do_job_analysis/$', views.do_job_analysis, name='do_jobs_analysis'),
    url(r'^poll_job_analysis/$', views.poll_jobs_analysis, name='poll_jobs_analysis')
]