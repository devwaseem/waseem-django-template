# Shared UI And Uploads

This project keeps reusable server-rendered UI in
`hyper/shared/components/ui/` and small browser controllers in
`hyper/shared/js/alpine/`.

Prefer these shared components before adding route-local markup. Keep business
rules in `app/` and pass template-ready values into the component.

## File Upload Dropzone

Use `hyper/shared/components/ui/file-upload-dropzone/index.html` for
drag-and-drop file inputs with a progress/status summary.

The component is intentionally state-agnostic: the page owns the Alpine state
and passes bindings/handlers into the component.

{% raw %}

```django
{% include "hyper/shared/components/ui/file-upload-dropzone/index.html" with
    label="Upload spreadsheet"
    input_ref="proposalFileInput"
    input_name="proposal_file"
    accept=".xlsx,.xls"
    multiple=False
    drag_class_binding="isDragging ? 'border-primary bg-primary/5' : ''"
    dragover_handler="isDragging = true"
    dragleave_handler="isDragging = false"
    drop_handler="handleDrop($event)"
    change_handler="handleFileChange($event)"
    input_disabled_binding="isSubmitting"
    button_disabled_binding="isSubmitting"
    summary_visible_binding="selectedFileName"
    file_name_binding="selectedFileName"
    file_state_binding="uploadState"
    progress_visible_binding="isSubmitting"
    progress_text_binding="uploadProgressText"
    progress_style_binding="`width: ${uploadProgress}%`"
    dropzone_title="Drop file here or choose one from your device"
    help_text="Accepted formats: .xlsx and .xls"
    button_label="Select file"
%}
```

{% endraw %}

Expected Alpine state shape:

```ts
{
    isDragging: false,
    isSubmitting: false,
    selectedFileName: '',
    uploadState: '',
    uploadProgress: 0,
    uploadProgressText: '',
}
```

Use clear names for upload handlers in the owning page, such as
`handleDrop`, `handleFileChange`, and `submitUpload`.

## Search Select

Use `hyper/shared/components/ui/search-select/index.html` when a page needs a
compact searchable select backed by a hidden form value.

The Alpine controller is registered globally as `searchSelect` from
`hyper/shared/js/main.head.ts`.

The component expects `options_json` to be a JSON array of objects with
`key` and `label` strings.

{% raw %}

```python
import json

context = {
    "assignee_options_json": json.dumps(
        [
            {"key": str(user.pk), "label": user.email}
            for user in users
        ]
    ),
}
```

```django
{% include "hyper/shared/components/ui/search-select/index.html" with
    input_id="assignee-select"
    hidden_name="assignee_id"
    selected_key=form.assignee_id.value|default_if_none:""
    query=selected_assignee_label|default:""
    options_json=assignee_options_json
    on_choose="submitAssigneeChange()"
    input_class=""
    placeholder="Search assignee"
    toggle_label="Toggle assignee options"
    no_results_text="No matches"
    invalid_message="Choose an option from the list"
%}
```

{% endraw %}

Use `on_choose=""` when choosing an option should not trigger a side effect.

## Icons

Shared UI uses Iconify classes with Lucide icons, for example:

```html
<span class="icon-[lucide--folder-open] h-4 w-4" aria-hidden="true"></span>
```

The template includes `@iconify-json/lucide` so these classes are available to
Tailwind/Iconify during `npm run build`.

## Upload Filename Safety

Use `app.helpers.files.safe_file_name` before storing user-provided filenames
in display fields, download headers, or metadata columns.

```python
from app.helpers.files import safe_file_name

display_name = safe_file_name(uploaded_file.name or "", fallback="attachment")
```

The helper trims blank names, applies a fallback, limits filenames to 255
characters, and preserves a suffix when truncating.

## Media Storage

Local media files use `MEDIA_ROOT`, and tests override default file storage to
a temporary directory via `app/conftest.py`.

For S3-backed media, keep object prefixes separate from local filesystem paths:
`MEDIA_LOCATION` remains the storage prefix, while `MEDIA_ROOT` is for local
filesystem serving and development URLs.
