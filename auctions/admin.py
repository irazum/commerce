from django.contrib import admin
from .models import User, Categories, Listings, Bids, Comments
# from django.forms import TextInput, Textarea
# from django.db import models


class ListingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'title', 'category', 'seller')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'comment_view']

    # # need to change view of the data in “add” and “change” admin-pages
    # formfield_overrides = {
    #     models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    # }

    # # if we use the funcs, we loss ability to sort column in admin panel
    # def listing_id(self, obj):
    #     return obj.listing.pk
    #
    # def listing_title(self, obj):
    #     return obj.listing.title


class BidsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'cost')


# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)




