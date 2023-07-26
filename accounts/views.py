from sqlite3 import IntegrityError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from accounts.forms import RegisterForm, UserUpdateView
from movie_app.models import Person


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # autentykacja
        if user is not None:
            login(request, user)  # autoryzacja
            redirect_url = request.GET.get('next', 'index')
            return redirect(redirect_url)
        return render(request, 'accounts/login.html')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'form2.html', {'form':form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('index')
        return render(request, 'form2.html',{'form':form})



class UserListView(ListView):

    model = User
    template_name = 'accounts/user_list.html'


class UpdateUserView(UpdateView):
    model = User
    template_name = 'form2.html'
    form_class = UserUpdateView

    def get_success_url(self):
        return reverse('update_user', kwargs={'pk':self.object.pk})


