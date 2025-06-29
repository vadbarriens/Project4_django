from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from message.forms import MessageForm
from message.models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'mail_messages'


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'add_message.html'
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'add_message.html'
    success_url = reverse_lazy('message:message_list')

    def dispatch(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Вы не можете редактировать сообщения.')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('message:message_list')

    def dispatch(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Вы не можете удалять сообщения.')
