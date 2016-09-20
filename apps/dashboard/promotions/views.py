import itertools
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.utils.text import ugettext_lazy as _
from django.views import generic
from oscar.forms.widgets import ImageInput
from oscar.apps.promotions.models import PagePromotion, MultiImage, Image
from oscar.apps.dashboard.promotions.views import UpdateView as CoreUpdateView
from oscar.apps.dashboard.promotions.views import DeleteView, CreateView
from apps.promotions.models import MultiHTML
from .forms import ImageFormSet, PromotionTypeSelectForm as SelectForm
from .conf import PROMOTION_CLASSES


class CreateRedirectView(generic.RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        code = self.request.GET.get('promotion_type', None)
        urls = {}
        for klass in PROMOTION_CLASSES:
            urls[klass.classname()] = reverse('dashboard:promotion-create-%s' %
                                              klass.classname())
        return urls.get(code, None)


class ListView(generic.TemplateView):
    template_name = 'dashboard/promotions/promotion_list.html'

    def get_context_data(self):
        # Need to load all promotions of all types and chain them together
        # no pagination required for now.
        data = []
        num_promotions = 0
        for klass in PROMOTION_CLASSES:
            objects = klass.objects.all()
            num_promotions += objects.count()
            data.append(objects)
        promotions = itertools.chain(*data)
        ctx = {
            'num_promotions': num_promotions,
            'promotions': promotions,
            'select_form': SelectForm(),
        }
        return ctx


class UpdateView(CoreUpdateView):
    def add_to_page(self, promotion, request, *args, **kwargs):
        instance = PagePromotion(content_object=self.get_object())
        form = self.link_form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            page_url = form.cleaned_data['page_url']
            instance.page_url = page_url
            instance.save()
            messages.success(request, _("Content block '%(block)s' added to"
                                        " page '%(page)s'")
                             % {'block': promotion.name,
                                'page': page_url})
            return HttpResponseRedirect(reverse('dashboard:promotion-update',
                                                kwargs=kwargs))

        main_form = self.get_form_class()(instance=self.object)
        ctx = self.get_context_data(form=main_form)
        ctx['link_form'] = form
        return self.render_to_response(ctx)


class UpdateMultiImageView(UpdateView):
    model = MultiImage
    fields = ['id', 'name']

    def get_context_data(self, formset=None, *args, **kwargs):
        ctx = super(UpdateMultiImageView, self).get_context_data(*args, **kwargs)
        if formset is None:
            ctx['image_formset'] = ImageFormSet(queryset=self.get_object().images.all())
        else:
            ctx['image_formset'] = formset
        return ctx

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        if action in self.actions:
            self.object = self.get_object()
            return getattr(self, action)(self.object, request, *args, **kwargs)
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.object)
        formset = ImageFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def form_valid(self, form, formset):
        self.object = self.get_object()
        self.object = form.save()
        if formset.is_valid():
            images = formset.save()
            for image in images:
                if image not in self.object.images.all():
                    self.object.images.add(image)
        return super(UpdateMultiImageView, self).form_valid(form)


class CreateMultiHTMLView(CreateView):
    model = MultiHTML
    fields = ['name']


class UpdateMultiHTMLView(UpdateView):
    model = MultiHTML
    fields = ['name', 'raw_htmls']


class DeleteMultiHTMLView(DeleteView):
    model = MultiHTML
