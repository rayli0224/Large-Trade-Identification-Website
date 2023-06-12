from django.contrib import admin

# Register your models here.

from .models import User, Stock
from .views import notify_users
admin.site.register(User)
admin.site.register(Stock)


#notify_users() don't do this all the time