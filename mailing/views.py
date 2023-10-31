import random

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import Message, Mailing, Client, Log


def home(request):

    blog_list = Blog.objects.all()
    blog_list = list(blog_list)
    random.shuffle(blog_list)

    context = {
        'title': 'Главная',
        'mailings': len(Mailing.objects.all()),
        'mailings_is_active': len(Mailing.objects.filter(mailing_status='launched')),
        'unique_clients_count': Client.objects.values('email').count(),
        'random_blog_list': blog_list
    }

    return render(request, 'mailing/home.html', context)


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        if self.request.user.is_staff:
            return Client.objects.all()
        else:
            return Client.objects.filter(creator=self.request.user.pk)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        message = form.save()
        message.creator = self.request.user
        message.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        elif self.request.user.is_staff:
            return self.object
        else:
            return None


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        else:
            return None


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        else:
            return Message.objects.filter(creator=self.request.user.pk)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        message.creator = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        elif self.request.user.is_staff:
            return self.object
        else:
            return None


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        else:
            return None


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(creator=self.request.user.pk)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        mailing.creator = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        elif self.request.user.is_staff:
            return self.object
        else:
            return None


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        elif self.request.user.is_staff:
            return self.object
        else:
            return None


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user:
            return self.object
        else:
            return None


def toggle_mailing_activity(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)

    if mailing_item.mailing_status == 'created' or mailing_item.mailing_status == 'completed':
        mailing_item.mailing_status = 'launched'
    else:
        mailing_item.mailing_status = 'completed'

    mailing_item.save()

    return redirect(reverse('mailing:mailing_detail', args=[mailing_item.pk]))


class LogListView(ListView):
    model = Log
