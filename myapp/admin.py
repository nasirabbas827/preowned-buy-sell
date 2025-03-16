from django.contrib import admin
from django.http import HttpResponse
from .models import Profile , Order , Transaction , Product , Category , Report


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Report)
