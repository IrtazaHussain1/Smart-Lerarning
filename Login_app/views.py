from django.shortcuts import render,redirect,get_object_or_404, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from Login_app.forms import Profile,UserRegisterForm
from django.contrib.auth.models import User
from .models import *
from dashboard_app.models import Subject

# Create your views here.
#create logout view
def Logout_views(request):
    logout(request)
    return redirect('/')
# create view for login form
def Login_View(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            paswrd = request.POST['pwd']
            user = authenticate(request, username=username, password=paswrd)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    name = User.objects.get(username=request.user)
                    request.session['username'] = username
                    return redirect('/dashboard/',{'name':name.username})
                else:
                     return render(request, 'login_app/index.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'login_app/index.html', {'error_message': 'Invalid login'})
        else:
            return render(request, 'login_app/index.html')


#create view for register form
def Reg_View(request):
    registered = False
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        profile_form=Profile(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = user_form.save()
                user.refresh_from_db()
                user.first_name=user_form.cleaned_data.get('first_name')
                user.last_name=user_form.cleaned_data.get('last_name')
                user.email=user_form.cleaned_data.get('email')
                user.save()
                user.refresh_from_db()
                p_save=profile_form.save(commit=False)
                p_save.t_teacher=user
                p_save.save()
                registered = True
                user_form = UserRegisterForm()
                profile_form=Profile()
                return render(request,'login_app/regform.html',{'user_form':user_form, 'profile_form':profile_form ,'registered':registered ,'message':'Registerd Successfully'})
            except Exception as e:
                registered = False
                user_form = UserRegisterForm()
                profile_form=Profile()
                return render(request,'login_app/regform.html',{'user_form':user_form, 'profile_form':profile_form ,'registered':registered ,'error_message':str(e)})
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserRegisterForm()
        profile_form=Profile()
    return render(request,'Login_app/regform.html',{'user_form':user_form, 'profile_form':profile_form ,'registered':registered })
