# chat/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.contrib.auth.models import User

@login_required
def index(request):
    return render(request, 'chat/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



@login_required
def index(request):
    user_chats = request.user.chats.all()
    return render(request, 'chat/index.html', {'chats': user_chats})

@login_required
def chat_detail(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = chat.messages.order_by('timestamp')
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def create_chat(request):
    if request.method == 'POST':
        usernames = request.POST.getlist('users')
        users = User.objects.filter(username__in=usernames)
        chat = Chat.objects.create()
        chat.participants.add(*users, request.user)
        chat.save()
        return redirect('chat_detail', chat_id=chat.id)
    
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/create_chat.html', {'users': all_users})
