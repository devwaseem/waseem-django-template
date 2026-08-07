# Email

Application email is authored in MJML and rendered by MRML, the Rust MJML
renderer. Use `{{ cookiecutter.project_slug }}.platform.emails.send_mjml_email`
for product mail.

The template deliberately does not provide an email layout, branding, or sample
message. When the product first needs email, create
`templates/email/base.mjml` at the project root. Django searches this
product-owned directory before platform templates. The base then owns the
document, brand, typography, layout, and footer; child templates provide only
their purpose-specific preview and content. Do not duplicate an email layout,
construct HTML in Python, or send HTML-only mail.

Write each child email in the voice suitable to its use case: clear operational
instructions for account/security messages, concise transactional detail for
receipts, and explicit context/action/deadline language for workflow notices.
Keep user-provided data escaped by Django templates and never interpolate it
into raw MJML attributes or HTML.
