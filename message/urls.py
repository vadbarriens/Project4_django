from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from message.apps import MessageConfig
from message.views import (
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
)

app_name = MessageConfig.name

urlpatterns = [
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/new/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
