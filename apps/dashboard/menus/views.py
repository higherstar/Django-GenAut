from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import MenuNode
from .forms import MenuNodeForm


class MenuNodeCreateView(CreateView):
    model = MenuNode
    form_class = MenuNodeForm
    template_name = 'dashboard/menus/menu_form.html'

    def get_success_url(self):
        if 'parent' in self.kwargs:
            return reverse('menus:menu-list-child', kwargs={'pk': self.kwargs['parent']})
        else:
            return reverse('menus:menu-list')

    def get_context_data(self, *args, **kwargs):
        ctx = super(MenuNodeCreateView, self).get_context_data(*args, **kwargs)
        if 'parent' in self.kwargs:
            ctx['object'] = get_object_or_404(MenuNode, pk=self.kwargs['parent'])
        return ctx

    def get_initial(self):
        initial = super(MenuNodeCreateView, self).get_initial()
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class MenuNodeUpdateView(UpdateView):
    model = MenuNode
    form_class = MenuNodeForm
    template_name = 'dashboard/menus/menu_form.html'

    def get_success_url(self):
        if self.object.is_root():
            return reverse('menus:menu-list')
        else:
            return reverse('menus:menu-list-child', kwargs={'pk': self.object.get_parent().pk})


class MenuNodeDeleteView(DeleteView):
    model = MenuNode
    template_name = 'dashboard/menus/menu_delete.html'

    def get_success_url(self):
        if self.object.is_root():
            return reverse('menus:menu-list')
        else:
            return reverse('menus:menu-list-child', kwargs={'pk': self.object.get_parent().pk})


class MenuNodeListView(ListView):
    model = MenuNode
    template_name = 'dashboard/menus/menu_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(MenuNodeListView, self).get_context_data(*args, **kwargs)
        if 'pk' in self.kwargs:
            ctx['object'] = get_object_or_404(MenuNode, pk=self.kwargs['pk'])
            ctx['object_list'] = ctx['object'].get_children()
        else:
            ctx['object_list'] = self.model.get_root_nodes()
        return ctx
