from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Message


@login_required
def home(request):
    messages = Message.objects.filter(sender=request.user)
    return render(request, 'messenger/home.html', {'messages': Message.objects.all()})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'messenger/signup.html', {'form': form})

@login_required
def message_create(request):
    users = User.objects.all()
    return render(request, 'messenger/message_create.html', {'users': users})

@login_required
def message_edit(request):
    return redirect(request, 'messenger/message_edit.html')

@login_required
def message_save(request):
    sender = request.user
    text = request.POST.get('message')
    receiver_username = request.POST.get('recipient')
    receiver = User.objects.get(username=receiver_username)
    m = Message(text=text,
                sent=True,
                sender=sender,
                receiver=receiver)
    m.save()
    return redirect('/inbox.html')

def sent(request):
    filteredMessageObjects = Message.objects.filter(sender=request.user)
    return render(request, 'messenger/sent.html', {'filteredMessageObjects': filteredMessageObjects})







def inbox(request):
    filteredMessageObjects = Message.objects.filter(receiver=request.user)
    return render(request, 'messenger/inbox.html', {'filteredMessageObjects': filteredMessageObjects, 'user': request.user})



