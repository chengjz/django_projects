from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string

from citys.models import City, State
from citys.forms import StateForm

# Create your views here.

class CityList(LoginRequiredMixin, View) :
    def get(self, request):
        sc = State.objects.all().count();
        cl = City.objects.all();

        ctx = { 'state_count': sc, 'city_list': cl };
        return render(request, 'citys/city_list.html', ctx)

class StateView(LoginRequiredMixin,View) :
    def get(self, request):
        sl = State.objects.all();
        ctx = { 'state_list': sl };
        return render(request, 'citys/state_list.html', ctx)

class StateCreate(LoginRequiredMixin, View):
    template = 'citys/state_form.html'
    success_url = reverse_lazy('citys')
    def get(self, request) :
        form = StateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request) :
        form = StateForm(request.POST)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        state = form.save()
        return redirect(self.success_url)

class StateUpdate(LoginRequiredMixin, View):
    model = State
    success_url = reverse_lazy('citys')
    template = 'citys/state_form.html'
    def get(self, request, pk) :
        state = get_object_or_404(self.model, pk=pk)
        form = StateForm(instance=state)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        state = get_object_or_404(self.model, pk=pk)
        form = StateForm(request.POST, instance = state)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)

class StateDelete(LoginRequiredMixin, DeleteView):
    model = State
    success_url = reverse_lazy('citys')
    template = 'citys/state_confirm_delete.html'

    def get(self, request, pk) :
        state = get_object_or_404(self.model, pk=pk)
        form = StateForm(instance=state)
        ctx = { 'state': state }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        state = get_object_or_404(self.model, pk=pk)
        state.delete()
        return redirect(self.success_url)

# Take the easy way out on the main table
class CityCreate(LoginRequiredMixin,CreateView):
    model = City
    fields = '__all__'
    success_url = reverse_lazy('citys')

class CityUpdate(LoginRequiredMixin, UpdateView):
    model = City
    fields = '__all__'
    success_url = reverse_lazy('citys')

class CityDelete(LoginRequiredMixin, DeleteView):
    model = City
    fields = '__all__'
    success_url = reverse_lazy('citys')

