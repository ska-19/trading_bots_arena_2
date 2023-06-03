from django.contrib import admin

from .models import Bot
from .models import Transaction

admin.site.register(Bot)
admin.site.register(Transaction)
