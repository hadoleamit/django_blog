from django.contrib import admin
from django.urls import path

from .views import(
    
    post_list,
    post_create,
    post_details,
    post_update,
    post_delete,
    author_details,
    post_vote,

    )
app_name = 'posts'

urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create),
    path('<int:id>', post_details, name='detail'),
    path('<int:id>/edit/', post_update, name='update'),
    path('<int:id>/delete/', post_delete),
    path('<int:id>/author/', author_details, name='author_details'),
    path('post_vote/', post_vote, name='post_vote'),
]                                                                                                                                                                                                                                                                                                                                          
