# your_app/context_processors.py

from .models import *
from userprofile.models import *


def menu_items(request):
    menu = []
    unread_notification_count = 0

    if request.user.is_authenticated:
        items = MenuItem.objects.all().order_by('order')
        unread_notification_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        items = MenuItem.objects.filter(authenticated_only=False).order_by('order')

    for item in items:
        menu_item = {
            'name': item.name,
            'url': item.get_url(request.user),
            'icon': item.icon,
        }
        menu.append(menu_item)

    return {
        "menu_items": menu,
        "unread_notification_count": unread_notification_count
    }

# def footer_info(request):
#     try:
#         social_links = SocialMediaLink.objects.all()
#     except SocialMediaLink.DoesNotExist:
#         social_links = []

#     return {'social_links': social_links}