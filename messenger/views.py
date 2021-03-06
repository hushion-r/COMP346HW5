from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Message


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
def inbox(request):
    """ shows all received messages """
    filtered_message_objects = Message.objects.filter(receiver=request.user, sent=True)
    return render(request, 'messenger/inbox.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def sent(request):
    """ shows all sent messages """
    filtered_message_objects = Message.objects.filter(sender=request.user, sent=True)
    return render(request, 'messenger/sent.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def drafts(request):
    """ shows all drafted messages """
    filtered_message_objects = Message.objects.filter(sender=request.user, sent=False)
    for draft in filtered_message_objects:
        print(draft)
    return render(request, 'messenger/drafts.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def message_create(request):
    """ takes old message. form to send message/save message as draft """
    users = User.objects.all()
    return render(request, 'messenger/message_create.html', {'users': users})

@login_required
def message_save(request):
    """ sends message/save message as draft by creating new Message object. interacts with 'message_create.html' """
    sender = request.user
    text = request.POST.get('message')
    receiver_username = request.POST.get('recipient')
    receiver = User.objects.get(username=receiver_username)
    if request.POST.get('submit'):
        m = Message(text=text,
                    sent=True,
                    sender=sender,
                    receiver=receiver)
        m.save()
        return redirect('/sent.html')
    else:   # elif request.POST.get('save')
        m = Message(text=text,
                    sent=False,
                    sender=sender,
                    receiver=receiver)

    m.save()
    return redirect('/inbox.html')

@login_required
def message_edit(request):
    """ takes old message. form to send message/save message as draft """
    users = User.objects.all()
    id = request.POST.get('message_edit')
    message = Message.objects.filter(id=id)
    return render(request, 'messenger/message_edit.html', {'users': users, 'message': message[0]})

@login_required
def message_update(request, message_id):
    """ loads draft message. sends message/save message as draft by updating Message object.
    interacts with 'message_edit.html' """
    old_message = Message.objects.filter(id=message_id)[0]
    old_message.sender = request.user
    old_message.text = request.POST.get('message')
    receiver_username = request.POST.get('recipient')
    old_message.receiver = User.objects.get(username=receiver_username)
    if request.POST.get('submit'):
        old_message.sent = True
        old_message.save()
        return redirect('/sent')
    else:   # elif request.POST.get('save')
        old_message.sent = False
    old_message.save()
    return redirect('/inbox.html')
