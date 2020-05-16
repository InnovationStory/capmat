from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from classroom.models import Quiz, Student
from django.shortcuts import get_object_or_404


class CommentNoticeListView(LoginRequiredMixin, ListView):
    "" "notification list" ""
    #Name of the context
    context_object_name = 'notices'
    #Template location
    template_name = 'notice/list.html'
    #Login redirection
    login_url = '/userprofile/login/'

    #Query set for unread notifications
    def get_queryset(self):
        return self.request.user.notifications.unread()

class CommentNoticeListView_read(LoginRequiredMixin, ListView):
    "" "notification list" ""
    #Name of the context
    context_object_name = 'notices'
    #Template location
    template_name = 'notice/inbox.html'
 
    #Query set for unread notifications
    def get_queryset(self):
        return self.request.user.notifications.unread()

   
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CommentNoticeListView_read, self).get_context_data(**kwargs)
        # Add in the publisher
        context['reads'] = self.request.user.notifications.read()
        return context

    

class CommentNoticeUpdateView(View):
    "" "update notification status" ""
    #Processing get requests
    def get(self, request):
        #Get unread message
        notice_id = request.GET.get('notice_id')
        #Update single notice
        if notice_id:
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect('notice:inbox')
        #Update all notifications
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:inbox')



class ExpertNoticeUpdateView(View):
    "" "update notification status" ""
    #Processing get requests
    def get(self, request):
        #Get unread message
        notice_id = request.GET.get('notice_id')
        #Update single notice
        if notice_id:
            article = get_object_or_404(Student,pk=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect('students:projet_detail', article.slug  )
        #Update all notifications
        else:
            return redirect('notice:list')