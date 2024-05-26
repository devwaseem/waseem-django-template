from drf_spectacular.extensions import OpenApiAuthenticationExtension


class APIKeyAuthenticationScheme(OpenApiAuthenticationExtension):  # type: ignore
    # full import path OR class ref
    target_class = "{{cookiecutter.project_name}}.auth.APIKeyAuthentication"
    name = "API Key"  # name used in the schema

    def get_security_definition(  # type: ignore
        self,
        auto_schema,  # noqa
    ) -> dict[str, str]:
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
