from email import message
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from vaparkarte.models import *
from .help import send_forgot_mail 
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

#pass_ritz:- ritesh23
# Create your views here.

def index(request) :
    return render(request, 'index.html')
    

def loginuser(request) :
    try:
        if request.method == 'POST':
            username = request.POST.get('uname')
            password = request.POST.get('password')
            print(username, password)

            #checking both field are entered
            if not username or not password:
                message.success(request, "Both Username And Password Required.")
                return redirect('/login')
            #checking username is exits or not
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                message.success(request, "User Not Found.")
                return redirect('/login')
            #checking user creditional        
            user = authenticate(username=username, password=password)

            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return redirect('/login')
            else:
                message.success(request,"Wrong Password Entered.")
                # No backend authenticated the credentials
                return redirect('/login')         
        #return HttpResponse("Login page")
    except Exception as e:
        print(e)
    return render(request, 'login.html')



def registeruser(request) :
    try:
        if request.method == 'POST':
            username = request.POST.get('uname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(username,email, password)

        try:
            #checking username is exits or not
            if User.objects.filter(username=username).first():
                message.success(request, "User Is Taken.")
                return redirect('/register')
            #checking email is exits or not
            if User.objects.filter(email=email).first():
                message.success(request, "Email Is Taken.")
                return redirect('/register')
            #saving User
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            #saving Profile        
            profile_obj=Profile.objects.create(user = user_obj)
            profile_obj.save()
            return redirect('/login')
        except Exception as e:
            print(e)
    except Exception as e:
            print(e)
    return render(request, 'register.html')


def change_pass(request,token):
    context={}
    try:
        profile_obj=Profile.objects.get(forgot_pass_token= token)
        print(profile_obj)

        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')

        
    except Exception as e:
        print(e)
    return render(request, 'change.html', context)

def forgot_pass(request):
    try:
        if request.method=='POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                message.success(request, "Not User Found")
                return redirect('/forgot')
            
            user_object=User.objects.get(username=username)
            token=str(uuid.uuid4())

            profile_obj= Profile.objects.get(user = user_object)
            profile_obj.forget_password_token = token
            profile_obj.save()

            send_forgot_mail(user_object,token)

            message.success(request, "Email s send to {{request.email}}")
            return redirect('/forgot')
        
        
    except Exception as e:
            print(e) 
    return render(request,'forgot.html')

def logoutuser(request) :
    logout(request)
    return redirect('/login')
    #return HttpResponse("Logout page")