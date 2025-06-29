from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from recipient.apps import RecipientConfig
from recipient.views import RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView, \
    RecipientDeleteView

app_name = RecipientConfig.name

urlpatterns = [
                  path('recipient/', RecipientListView.as_view(), name='recipient_list'),
                  path('recipient/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
                  path('recipient/new/', RecipientCreateView.as_view(), name='recipient_create'),
                  path('recipient/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_edit'),
                  path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
