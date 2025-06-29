from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from recipient.forms import RecipientForm
from recipient.models import Recipient


class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if self.request.user.has_perm('mailings.can_see_all_recipients'):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'recipient_detail.html'
    context_object_name = 'recipient'


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'add_recipient.html'
    success_url = reverse_lazy('recipient:recipient_list')

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'add_recipient.html'
    success_url = reverse_lazy('recipient:recipient_list')

    def dispatch(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Вы не можете редактировать получателя рассылки.')


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient:recipient_list')

    def dispatch(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Вы не можете удалять получателя рассылки.')
