from django import template
from django.template.defaultfilters import stringfilter


register=template.Library()

@register.filter
def divide(string, args):
    return int(int(string)/int(args)) + 1

@register.filter
def listcarousal(string):
    return [ i for i in range(int(string))]


    



