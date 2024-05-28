from django import template

from discussion_forums.views import get_profile_pic_url

register = template.Library()


@register.filter
def get_profile_picture_url(user_profile):
    return get_profile_pic_url(user_profile)
