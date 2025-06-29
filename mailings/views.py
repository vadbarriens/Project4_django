from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages

from message.models import Message
from .management.commands.send_message import send_mailing
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from mailings.forms import MailingForm
from mailings.models import Mailing, MailingAttempt
from recipient.models import Recipient


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.has_perm('mailings.can_see_all_mailings'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_manager = self.request.user.groups.filter(name="Manager").exists()
        context["is_manager"] = is_manager
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'add_mailing.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        owner = self.request.user
        form.fields['recipients'].queryset = Recipient.objects.filter(owner=owner)
        form.fields['message'].queryset = Message.objects.filter(owner=owner)
        return form


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'add_mailing.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def dispatch(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Вы не можете редактировать рассылки.')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        owner = self.request.user
        form.fields['recipients'].queryset = Recipient.objects.filter(owner=owner)
        form.fields['message'].queryset = Message.objects.filter(owner=owner)
        return form


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def dispatch(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Вы не можете удалять рассылки.')


def home_view(request):
    total_mail = Mailing.objects.count()
    active_mail = Mailing.objects.filter(status='LA').count()
    unique_recipients = Recipient.objects.values('email').distinct().count()

    context = {
        'total_mail': total_mail,
        'active_mail': active_mail,
        'unique_recipients': unique_recipients,
    }

    return render(request, 'home.html', context)


class MailingStatisticsView(ListView):
    model = Mailing
    template_name = 'mailing_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = Mailing.objects.filter(owner=self.request.user)
        mailing_stats = []
        for mailing in mailings:
            stats = {
                'mailing': mailing,
                'successful_attempts_count': mailing.mailing_attempts.filter(
                    status=MailingAttempt.SUCCESSFULLY).count(),
                'failed_attempts_count': mailing.mailing_attempts.filter(status=MailingAttempt.FAILED).count(),
                'total_sent_messages': mailing.mailing_attempts.count(),
            }
            mailing_stats.append(stats)

        context['mailing_stats'] = mailing_stats
        return context


class SendMailingView(View):
    def post(self, request, *args, **kwargs):
        mailing_id = kwargs.get('pk')
        mailing = Mailing.objects.get(pk=mailing_id)

        try:
            send_mailing(mailing)
            messages.success(request, 'Рассылка успешно отправлена!')
        except Exception as e:
            messages.error(request, f'Ошибка при отправке рассылки: {str(e)}')

        return HttpResponseRedirect(reverse('mailings:mailing_list'))


class MailingStopView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        user = request.user
        is_manager = user.groups.filter(name='Manager').exists()
        if is_manager or user == mailing.owner:
            mailing.status = 'CO'
            mailing.save()

            return redirect("mailings:mailing_list")
        return HttpResponseForbidden("У вас нет прав для отключения рассылки")


def mailing_list_view(request):
    mailings = Mailing.objects.filter(owner=request.user)
    return render(request, 'mailing_statistics.html', {'mailings': mailings})
