from django.contrib import admin
from .models import User, Categories, Listings, Bids

class ListingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'picture', 'category', 'seller')

# class BidsAdmin(admin.ModelAdmin):
#     list_display = ('cost', 'users', 'listings')

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids)





