
from ads.models import Ad

from django.views import View
from django.views import generic
from django.shortcuts import render

from ads.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class AdListView(OwnerListView):
    model = Ad
    template_name = "article_list.html"

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "article_detail.html"

class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title','price', 'text']
    template_name = "article_form.html"

class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title','price', 'text']
    template_name = "article_form.html"

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "article_delete.html"