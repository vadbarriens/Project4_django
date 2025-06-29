from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    home_view, MailingStopView, MailingStatisticsView, SendMailingView

app_name = MailingsConfig.name

urlpatterns = [
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', cache_page(60) (MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing/new/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('', home_view, name='home'),
    path("mailing/<int:pk>/stop", MailingStopView.as_view(), name="mailing_stop"),
    path('mailing/statistics/', MailingStatisticsView.as_view(), name='mailing_statistics'),
    path('mailing/<int:pk>/send/', SendMailingView.as_view(), name='send_mailing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
