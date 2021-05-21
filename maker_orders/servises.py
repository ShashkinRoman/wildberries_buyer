from django.shortcuts import render
from django.shortcuts import get_object_or_404

from maker_orders.models import Order


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, id_):
        obj = get_object_or_404(self.model, id=id_)
        return render(request, self.template, context={self.model.__name__.lower(): obj})
