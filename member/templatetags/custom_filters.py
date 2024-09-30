from django import template

register = template.Library()

@register.filter
def status_border_class(status):
    return {
        'Waiting for Approval': 'warning',
        'New Member': 'info',
        'Member': 'success',
        'Not a Member': 'danger'
    }.get(status, 'primary')

@register.filter
def status_text_class(status):
    return {
        'Waiting for Approval': 'warning',
        'New Member': 'info',
        'Member': 'success',
        'Not a Member': 'danger'
    }.get(status, 'primary')