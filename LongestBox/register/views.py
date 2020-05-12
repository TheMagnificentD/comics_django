from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register(response):
        if response.method == 'POST':
                form = RegisterForm(response.POST)
                if form.is_valid():
                        form.save()
                        return redirect('/confirm_registration')
        else:
                form = RegisterForm()
        return render(response,'register/register.html', {'form':form})

def conf_registration(response):
        return render(response, 'register/confirm_registration.html',{})
