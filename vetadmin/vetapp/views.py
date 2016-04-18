"""Create your views here."""

from django.shortcuts import render
from django.views.generic import TemplateView

from .models import CarouselSlide


class IndexView(TemplateView):
    """Index."""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['slides'] = CarouselSlide.objects
        return ctx
