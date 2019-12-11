from register.models import LoginUser
from django import template

register = template.Library()


@register.simple_tag
def is_leader(username):
    leader = LoginUser.objects.filter(username=username).values('is_leader')
    return leader[0]['is_leader']


# def status_operation():