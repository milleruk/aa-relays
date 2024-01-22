from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class RelaysMenuItem(MenuItemHook):
    """ This class ensures only authorized users will see the menu entry """
    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _('relays'),
            'fa fa-cube fa-fw',
            'relays:index',
            navactive=['relays:index']
        )

    def render(self, request):
        if request.user.has_perm('relays.basic_access'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return RelaysMenuItem()


@hooks.register('url_hook')
def register_urls():
    return UrlHook(urls, 'relays', r'^relays/')


@hooks.register('discord_cogs_hook')
def register_cogs():
    return ["relays.cogs.relays"]
