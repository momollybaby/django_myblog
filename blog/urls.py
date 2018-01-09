from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_success/$', views.success, name='register_success'),
]
