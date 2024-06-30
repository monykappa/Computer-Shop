# your_app/context_processors.py

from .models import *


def menu_items(request):
    if request.user.is_authenticated:
        items = MenuItem.objects.all().order_by('order')
    else:
        items = MenuItem.objects.filter(authenticated_only=False).order_by('order')

    menu = []
    for item in items:
        url = item.get_url(request.user)
        print(f"Menu item: {item.name}, URL: {url}")  # Debug print statement
        menu.append({
            'name': item.name,
            'url': url,
            'icon': item.icon
        })

    return {"menu_items": menu}

# def footer_info(request):
#     try:
#         social_links = SocialMediaLink.objects.all()
#     except SocialMediaLink.DoesNotExist:
#         social_links = []

#     return {'social_links': social_links}