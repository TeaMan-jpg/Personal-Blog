from django import template
from django.contrib.auth.models import User, Permission,Group
register = template.Library()

@register.filter(name='has_group')
def has_group(user):
    return user.groups.filter(name="Moderator").exists()





