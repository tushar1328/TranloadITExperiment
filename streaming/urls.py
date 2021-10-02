from django.urls import path
from .views import StreamCreate, StreamUpdate, StreamDelete, stream_index

app_name = "stream"

urlpatterns = [
    path('', stream_index, name='stream_index'),
    path('stream/add', StreamCreate.as_view(), name='stream_form_create'),
    path('stream/edit/<str:pk>', StreamUpdate.as_view(), name='stream_form_edit'),
    path('stream/delete/<str:pk>', StreamDelete.as_view(), name='stream_form_remove'),
]
