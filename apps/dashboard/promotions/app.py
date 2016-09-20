from django.conf.urls import url
from oscar.apps.dashboard.promotions.app import PromotionsDashboardApplication as CorePromotionsDashboardApplication
from .views import UpdateMultiImageView, CreateMultiHTMLView, UpdateMultiHTMLView, DeleteMultiHTMLView


class PromotionsDashboardApplication(CorePromotionsDashboardApplication):
    update_multiimage_view = UpdateMultiImageView
    create_multihtml_view = CreateMultiHTMLView
    update_multihtml_view = UpdateMultiHTMLView
    delete_multihtml_view = DeleteMultiHTMLView

    def get_urls(self):
        urls = super(PromotionsDashboardApplication, self).get_urls()
        urls += [
            url(r'create/multihtml/', self.create_multihtml_view.as_view(), name='promotion-create-multihtml'),
            url(r'^update/(?P<ptype>multihtml)/(?P<pk>\d+)/$', self.update_multihtml_view.as_view(), name='promotion-update'),
            url(r'^delete/(?P<ptype>multihtml)/(?P<pk>\d+)/$', self.delete_multihtml_view.as_view(), name='promotion-delete')
        ]
        return self.post_process_urls(urls)


application = PromotionsDashboardApplication()
