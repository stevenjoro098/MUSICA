from django import template

register = template.Library()


@register.filter(name='user_info')
def user_info(user, group_name):
    return user.groups.filter(name=group_name).exists()
