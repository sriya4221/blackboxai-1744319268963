from django import template

register = template.Library()

@register.filter
def filter_company(visitors, company):
    return [visitor for visitor in visitors if visitor.company == company]

@register.filter
def filter_purpose(visitors, purpose):
    return [visitor for visitor in visitors if visitor.purpose == purpose]
