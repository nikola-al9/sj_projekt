from django.contrib import admin

# Register your models here.
from authentication.models import Account

admin.site.register(Account)