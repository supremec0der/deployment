from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$',views.login, name='login'),
    url(r'^dashboard$', views.dasboard, name='dasboard'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^user/(?P<id>\d+)$', views.user, name ='user'),
    url(r'^myaccount/(?P<id>\d+)$', views.edit, name ='edit'),
    url(r'^add_quote$', views.add_quote, name='add_quote'),
    url(r'^like$', views.like, name='like'),
    url(r'^update$', views.update, name ='update'),
    url(r'^(?P<id>\d+)/delete$', views.delete, name ='delete')
]