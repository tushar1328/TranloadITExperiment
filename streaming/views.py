from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from streaming.models import Stream


@login_required
def stream_index(request):
    context = dict()
    if request.user.is_superuser:
        stream = Stream.objects.all()
    else:
        stream = Stream.objects.filter(user=request.user)
    context['stream'] = stream
    return render(request, 'stream/stream_home.html', context=context)


class StreamCreate(CreateView):
    model = Stream
    success_url = reverse_lazy('stream:stream_index')
    template_name = "stream/stream_form.html"
    fields = ('file',)


class StreamUpdate(UpdateView):
    model = Stream
    success_url = reverse_lazy('stream:stream_index')
    template_name = "stream/stream_form.html"
    fields = ('file',)


class StreamDelete(DeleteView):
    model = Stream
    success_url = reverse_lazy('stream:stream_index')
    template_name = "stream/stream_delete.html"
