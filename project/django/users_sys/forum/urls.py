from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'forum'

urlpatterns = [
    path('add-post', CUDPostView.as_view()),
    path('edit-post', CUDPostView.as_view()),
    path('add-comment', CUDCommentView.as_view()),
    path('edit-comment', CUDCommentView.as_view()),
    path('posts', login_required(ListPostsView.as_view()), name='posts'),
    path('delete-post', CUDPostView.as_view()),
    path('delete-comment', CUDCommentView.as_view()),
]