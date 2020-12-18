from django.contrib import admin
from .models import User, Categories, Listings, Bids, Comments


class ListingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'title', 'category', 'seller')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'comment_view']


class BidsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'cost')


# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)




