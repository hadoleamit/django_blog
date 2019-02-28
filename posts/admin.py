from django.contrib import admin

# Register your models here.
from posts.models import Post, Comment, Author, Ratings 

class PostModelAdmin(admin.ModelAdmin):
    list_display=["title","timestamp","updated"]
    list_display_links=["updated"]
    list_editable=["title"]
    list_filter=["updated","timestamp"]
    search_fields=["title","content"]
    
    
    class Meta:
         model = Post

class CommentAdmin(admin.ModelAdmin):
    list_display=('user','Date')

class AuthorAdmin(admin.ModelAdmin):
    list_display=("user","mobile_no", "address", "date_of_birth")
    
    class Meta:
        model = Author    

class RatingsAdmin(admin.ModelAdmin):
    list_display=('post','no_of_ratings','no_of_users','average_rating')   

admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Ratings, RatingsAdmin)