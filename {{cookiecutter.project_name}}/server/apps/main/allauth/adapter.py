from typing import Any

from allauth.account.adapter import DefaultAccountAdapter

from server.apps.main.context_processors import get_site_data


class AllAuthAccountAdapter(DefaultAccountAdapter):  # type: ignore
    def send_mail(  # type: ignore
        self,
        template_prefix: str,
        email: str,
        context: dict[str, Any],
    ) -> None:
        context.update(get_site_data(request=self.request))
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    def format_email_subject(self, subject: str) -> str:
        site_data = get_site_data(request=self.request)
        prefix = site_data["site_name"]
        if prefix is None:
            return subject
        return f"{prefix}: {subject}"
