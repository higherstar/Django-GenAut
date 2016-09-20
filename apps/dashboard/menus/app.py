from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from oscar.core.application import Application

from apps.dashboard.menus import views


class MenusDashboardApplication(Application):
    name = 'menus'
    menu_node_list_view = views.MenuNodeListView
    menu_node_create_view = views.MenuNodeCreateView
    menu_node_update_view = views.MenuNodeUpdateView
    menu_node_delete_view = views.MenuNodeDeleteView

    def get_urls(self):
        urlpatterns = patterns(
            '',
            url(r'^$', self.menu_node_list_view.as_view(), name='menu-list'),
            url(r'^(?P<pk>\d+)/$', self.menu_node_list_view.as_view(), name='menu-list-child'),
            url(r'^create/$', self.menu_node_create_view.as_view(), name='menu-create-root'),
            url(r'^create/(?P<parent>\d+)/$', self.menu_node_create_view.as_view(), name='menu-create-child'),
            url(r'^edit/(?P<pk>\d+)/$', self.menu_node_update_view.as_view(), name='menu-update'),
            url(r'^delete/(?P<pk>\d+)/$', self.menu_node_delete_view.as_view(), name='menu-delete'),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = MenusDashboardApplication()
