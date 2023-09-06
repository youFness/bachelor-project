from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate ,login, logout
from .models import User
#from social_django.utils import psa
#from social_core.actions import do_auth
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company


#register applicant only
def register_applicant(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            var.is_applicant = True
            var.username = var.email
            var.save()
            Resume.objects.create(user=var)
            messages.info(request, 'Your account has been creates. Please login')
            return redirect('login')
        else:
            print(form.errors)
            messages.warning(request, 'Something went wrong')
            return redirect('register-applicant')
    else:
        form = RegisterUserForm()
        context = {'form':form}
        return render(request, 'users/register_applicant.html',context)
    

    #register recruiter only
def register_recruiter(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            var.is_recruiter = True
            var.username=var.email

            var.save()
            Company.objects.create(user=var)
            
            messages.info(request,'Your account has been created . Please login')
            return redirect('login')
        else:
            messages.warning(request,'Something went wrong')
            return redirect('register-recruiter')
    else:
        form = RegisterUserForm()
        context={'form':form}
        return render(request,'users/register_recruiter.html',context) 



    #login a user
def login_user(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
                    login(request,user)
                    return redirect('dashboard')
                    # if request.user.is_applicant:
                    #     return redirect('applicant-dashboard')
                    # elif request.user.is_recruiter:
                    #     return redirect('recruiter-dashboard')
                    # else :
                    #     return redirect('login')
        else:
                    messages.warning(request,'Something went wrong')
                    return redirect('login')    
    else:
            return render(request, 'users/login.html')
   
# @psa('social:complete')
# def social_login(request, backend):
#     """Social media authentication view"""
#     return do_auth(request.backend, redirect_name='social-login-callback')

# @psa('social:complete')
# def social_login_callback(request, backend):
#     """Social media authentication callback view"""
#     user = request.backend.do_auth(request.GET.get('access_token'))
#     if user:
#         login(request, user)
#         return redirect('dashboard')
#     else:
#         messages.warning(request, 'Social media authentication failed')
#         return redirect('login')

#logout a user

def logout_user(request):
    try:
        logout(request)
        messages.info(request, 'Your session has ended')
        return redirect('login')
    except Exception as e:
        messages.warning(request, 'An error occurred during logout')
        return redirect('login')


    
