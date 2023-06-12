from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('add_stock', views.add_stock, name='add_stock'),
    path('get_profile', views.get_profile, name='get_profile'),
    path('changepass',views.changepass,name='changepass'),
    path('removestock', views.removestock, name='removestock'),
    path('get_stocks', views.get_stocks, name='get_stocks')
]
