from django.contrib.messages import get_messages
from django_htmx.http import trigger_client_event


def add_messages_to_htmx(request, response):
    storage = get_messages(request)
    messages = [
        {"message": message.message, "tags": message.tags} for message in storage
    ]
    trigger_client_event(response, "notifyGlobal", {"data": messages})
