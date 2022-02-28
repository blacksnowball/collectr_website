from ..models.requests import NewItemRequest, NewCollectionRequest
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class newCollection(LoginRequiredMixin, CreateView):
    model = NewCollectionRequest
    fields = ['new_collection_name', 'description']
    success_url = reverse_lazy('index')
    template_name = 'requests/base_form_template.html'

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)


class newItem(LoginRequiredMixin, CreateView):
    model = NewItemRequest
    fields = ['new_item_name', 'add_to_collection', 'description']
    success_url = reverse_lazy('index')
    template_name = 'requests/base_form_template.html'

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)



