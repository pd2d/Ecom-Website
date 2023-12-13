from django.contrib import admin
from .models import Products, Company, Images, Orders
from nested_admin import NestedModelAdmin, NestedStackedInline

# Register your models here.

admin.site.register(Company)
admin.site.register(Orders)


class ProductsImageInline(NestedStackedInline):
    """
    PostImage inline
    """
    model = Images
    extra = 0                # No.empty forms to display for adding new PostImage
    can_delete = True        # to delete individual PostImage
    show_change_link = True  # display a change link for each PostImage instance

@admin.register(Products)                 #post module accessible from the admin panel
class ProductsAdmin(NestedModelAdmin):   #new admin class named PostsAdmin 
    """
    Admin panel config for Post
    """

    #list_display = ('company',)  #show the description of each post
    #list_filter = ('tags',)          #adds a filter allowing users to filter Post based on tags 
    inlines = (ProductsImageInline,)     #included as an inline within the PostsAdmin admin class
