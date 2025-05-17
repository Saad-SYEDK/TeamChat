from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from .models import Chat, Message
from django.contrib.auth.models import User

@login_required
def index(request):
    user_chats = request.user.chats.all()

    chats_with_other = []
    for chat in user_chats:
        if not chat.is_group:
            other_user = chat.participants.exclude(id=request.user.id).first()
        else:
            other_user = None
        
        # Count unread messages by checking read_by, NOT timestamp:
        unread_count = chat.messages.exclude(sender=request.user).exclude(read_by=request.user).count()

        chats_with_other.append((chat, other_user, unread_count))

    return render(request, 'chat/index.html', {'chats_with_other': chats_with_other})

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
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.select_related('sender').all()

    with transaction.atomic():
        for message in messages:
            if request.user != message.sender and request.user not in message.read_by.all():
                message.read_by.add(request.user)

    other_user = None
    if not chat.is_group:
        other_user = chat.participants.exclude(id=request.user.id).first()

    context = {
        'chat': chat,
        'messages': messages,
        'other_user': other_user,
    }
    return render(request, 'chat/chat_detail.html', context)

@login_required
def create_chat(request):
    if request.method == 'POST':
        is_group = request.POST.get('is_group') == 'on'
        selected_user_ids = request.POST.getlist('participants')
        chat_name = request.POST.get('name', '').strip()

        if is_group:
            if not chat_name:
                return render(request, 'chat/create_chat.html', {
                    'error': 'Group chat must have a name.',
                    'users': User.objects.exclude(id=request.user.id)
                })
            if len(selected_user_ids) < 2:
                return render(request, 'chat/create_chat.html', {
                    'error': 'Select at least two users for a group chat.',
                    'users': User.objects.exclude(id=request.user.id)
                })
        else:
            if len(selected_user_ids) != 1:
                return render(request, 'chat/create_chat.html', {
                    'error': 'Private chat must have exactly one user.',
                    'users': User.objects.exclude(id=request.user.id)
                })
            chat_name = None  # Set dynamically in chat list

        chat = Chat.objects.create(name=chat_name, is_group=is_group)
        chat.participants.add(request.user)
        for user_id in selected_user_ids:
            chat.participants.add(User.objects.get(id=user_id))
        return redirect('chat_detail', chat_id=chat.id)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/create_chat.html', {'users': users})

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content,
                timestamp=timezone.now()
            )
        return redirect('chat_detail', chat_id=chat.id)
    else:
        return redirect('chat_detail', chat_id=chat.id)
