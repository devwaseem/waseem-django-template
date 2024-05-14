import json
from enum import StrEnum
from pathlib import Path
from typing import Any

from django import template
from django.templatetags.static import static

from src.server.settings.common import BASE_DIR

register = template.Library()


def _get_manifest_data() -> dict[str, Any]:
    manifest_file = BASE_DIR / "dist/.vite/manifest.json"
    with manifest_file.open("r") as manifest_fd:
        return json.loads(manifest_fd.read())



class AssetFileNotFoundError(Exception):
    ...


def _get_script_and_css_tags(
    *,
    manifest_key: str,
) -> set[str]:
    manifest = _get_manifest_data()
    js_file = manifest[manifest_key].get("file")
    js_static_url = static(js_file)

    output = set()
    output.add(f"<script type='module' src='{js_static_url}'></script>")
    output.add(f"<link rel='modulepreload' href='{js_static_url}'></script>")
    if css_files := manifest[manifest_key].get("css"):
        for css_file in css_files:
            css_static_url = static(css_file)

            output.add(f"<link rel='stylesheet' href='{css_static_url}'>")

    if import_files := manifest[manifest_key].get("imports"):
        for file in import_files:
            output = output.union(
                set(_get_script_and_css_tags(manifest_key=file))
            )

    return output


class AssetResolverMode(StrEnum):
    LOCAL = "local"
    GLOBAL = "global"


class AssetTagNode(template.Node):
    def __init__(
        self,
        *,
        file_name_or_path: str,
        mode: AssetResolverMode,
    ) -> None:
        self.file_name_or_path = file_name_or_path
        self.mode = mode

    def render(self, context) -> str:  # noqa
        match self.mode:
            case AssetResolverMode.LOCAL:
                page_directory = str(Path(self.origin.name).parent).replace(
                    str(Path.cwd()) + "/", ""
                )
                if not (
                    Path.cwd() / page_directory / self.file_name_or_path
                ).exists():
                    raise AssetFileNotFoundError(
                        f"{self.file_name_or_path} not found "
                        "in local directory"
                    )

                return "".join(
                    _get_script_and_css_tags(
                        manifest_key=page_directory
                        + "/"
                        + self.file_name_or_path
                    )
                )

            case AssetResolverMode.GLOBAL:
                return "".join(
                    _get_script_and_css_tags(
                        manifest_key=str("assets/" + self.file_name_or_path),
                    )
                )


@register.tag(name="load_asset")
def load_asset(parser, token) -> AssetTagNode:  # noqa
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise ValueError(
            f"{token.contents.split()[0]} tag takes "
            "exactly 2 or more arguments"
        )

    mode = tokens[1]
    file_path = tokens[2]

    return AssetTagNode(
        file_name_or_path=file_path,
        mode=mode,
    )
