
from horses.models import Horse, Comment
from horses.forms import CreateForm, CommentForm

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.core.files.uploadedfile import InMemoryUploadedFile

from horses.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class HorseListView(OwnerListView):
    model = Horse
    template_name = "horse_list.html"

class HorseDetailView(OwnerDetailView):
    model = Horse
    template_name = "horse_detail.html"
    def get(self, request, pk) :
        horse = Horse.objects.get(id=pk)
        comments = Comment.objects.filter(horse=horse).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'horse' : horse, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class HorseFormView(OwnerUpdateView):
    template = 'horse_form.html'
    success_url = reverse_lazy('horses')

    def get(self, request, pk=None) :

        if pk is None:
            form = CreateForm()
            ctx = {'form': form}
            return render(request, self.template, ctx)
        else:
            horse = get_object_or_404(Horse, id=pk, owner=self.request.user)
            form = CreateForm(instance=horse)
            ctx = {'form': form}
            return render(request, self.template, ctx)


    def post(self, request, pk=None) :
        if pk is None:
            form = CreateForm(request.POST, request.FILES or None)

            if not form.is_valid():
                ctx = {'form': form}
                return render(request, self.template, ctx)

            # Add owner to the model before saving
            horse = form.save(commit=False)
            horse.owner = self.request.user
            horse.save()
            return redirect(self.success_url)
        else:
            horse = get_object_or_404(Horse, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=horse)

            if not form.is_valid():
                ctx = {'form': form}
                return render(request, self.template, ctx)

            horse.save()
            return redirect(self.success_url)


class HorseDeleteView(OwnerDeleteView):
    model = Horse
    template_name = "horse_delete.html"


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Horse, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, horse=f)
        comment.save()
        return redirect(reverse_lazy('horse_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        horse = self.object.horse
        return reverse_lazy('horse_detail', args=[horse.id])
