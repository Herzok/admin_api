from django.shortcuts import render, HttpResponse
from django.views import View
from users.mixins import *


class CUDCommentView(PermissionRequiredMixin, View):
    permission_required = ['add_comment','edit_comment','delete_comment']
    def get(self, request):
        return HttpResponse("Работа с комментарием проведена")
   
    
class ListPostsView(PermissionRequiredMixin, View):
    permission_required = ['read_post']
    def get(self, request):
        return HttpResponse("Выведен список")
    

class CUDPostView(PermissionRequiredMixin, View):
    permission_required = ['create_post','edit_post','delete_post']
    def get(self, request):
        return HttpResponse("Работа с постом проведена")
