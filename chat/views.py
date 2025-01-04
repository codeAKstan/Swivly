from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth.models import User

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})


@login_required
def start_conversation(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    # Check if a conversation already exists between these two users
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=recipient).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)

    return redirect('chat:conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Ensure the logged-in user is a participant
    if request.user not in conversation.participants.all():
        return redirect('chat:start_conversation', recipient_id=request.user.id)

    # Handle sending a message
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
        return redirect('chat:conversation_detail', conversation_id=conversation.id)

    messages = conversation.messages.order_by('created')
    return render(request, 'chat/conversation_detail.html', {'conversation': conversation, 'messages': messages})
