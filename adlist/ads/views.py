
from ads.models import Ad


from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class AdListView(OwnerListView):
    model = Ad
    template_name = "ad_list.html"

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ad_detail.html"

# class AdCreateView(OwnerCreateView):
#     model = Ad
#     fields = ['title','price', 'text']
#     template_name = "ad_form.html"
#
#     template = 'ad_form.html'
#     success_url = reverse_lazy('pics')
#     def get(self, request, pk=None) :
#         form = CreateForm()
#         ctx = { 'form': form }
#         return render(request, self.template, ctx)
#
#     def post(self, request, pk=None) :
#         form = CreateForm(request.POST, request.FILES or None)
#
#         if not form.is_valid() :
#             ctx = {'form' : form}
#             return render(request, self.template, ctx)
#
#         # Add owner to the model before saving
#         pic = form.save(commit=False)
#         pic.owner = self.request.user
#         pic.save()
#         return redirect(self.success_url)
#
#
# class AdUpdateView(OwnerUpdateView):
#     model = Ad
#     fields = ['title','price', 'text']
#     template_name = "ad_form.html"

class AdFormView(OwnerUpdateView):
    template = 'ad_form.html'
    success_url = reverse_lazy('ads')

    def get(self, request, pk=None) :

        if pk is None:
            form = CreateForm()
            ctx = {'form': form}
            return render(request, self.template, ctx)
        else:
            pic = get_object_or_404(Pic, id=pk, owner=self.request.user)
            form = CreateForm(instance=pic)
            ctx = {'form': form}
            return render(request, self.template, ctx)


    def post(self, request, pk=None) :
        if pk is None:
            form = CreateForm(request.POST, request.FILES or None)

            if not form.is_valid():
                ctx = {'form': form}
                return render(request, self.template, ctx)

            # Add owner to the model before saving
            pic = form.save(commit=False)
            pic.owner = self.request.user
            pic.save()
            return redirect(self.success_url)
        else:
            pic = get_object_or_404(Pic, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=pic)

            if not form.is_valid():
                ctx = {'form': form}
                return render(request, self.template, ctx)

            pic.save()
            return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "ad_delete.html"

def stream_file(request, pk) :
    pic = get_object_or_404(Pic, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response