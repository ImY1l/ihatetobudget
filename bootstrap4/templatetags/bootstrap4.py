from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def bootstrap_css(context, *args, **kwargs):
    # Minimal no-op stub for tests.
    return ""


@register.simple_tag(takes_context=True)
def bootstrap_javascript(context, *args, **kwargs):
    # Minimal no-op stub for tests.
    return ""


@register.simple_tag(takes_context=True)
def bootstrap_messages(context, *args, **kwargs):
    # Minimal no-op stub for tests.
    return ""


@register.simple_tag(takes_context=True)
def bootstrap_form(context, form, *args, **kwargs):
    """Render a Django form as-is.

    This project includes a lightweight bootstrap4 template tag library.
    Some templates expect `{% bootstrap_form form %}` and will 500 if the tag
    isn't registered.
    """
    return form.as_p()


@register.simple_tag(takes_context=True)
def bootstrap_button(context, *args, **kwargs):
    """Render a basic submit button.

    Supports the template usage: `{% bootstrap_button 'Label' button_type='submit' button_class='...' %}`.
    """
    label = args[0] if args else kwargs.get("label", "")
    button_type = kwargs.get("button_type", "button")
    button_class = kwargs.get("button_class", "btn btn-primary")
    return f"<button type=\"{button_type}\" class=\"{button_class}\">{label}</button>"


