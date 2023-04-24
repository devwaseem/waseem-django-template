from django.contrib.messages import get_messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event


def add_messages_to_htmx(request, response):
    storage = get_messages(request)
    messages = [
        {"message": message.message, "tags": message.tags} for message in storage
    ]
    trigger_client_event(response, "notifyGlobal", {"data": messages})


class HTMXLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self) -> HttpResponseRedirect | HttpResponseClientRedirect:
        redirect = super().handle_no_permission()
        if self.request.htmx:  # type:ignore
            redirect = redirect_to_login(self.request.htmx.current_url_abs_path)  # type: ignore
            return HttpResponseClientRedirect(redirect.url)
        return redirect

