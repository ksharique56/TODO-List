from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
from .forms import * 
# Create your views here.

def index(request):
    tasks = Task.objects.all()

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'tasks': tasks, 'form': form}
    return render(request,'task/list.html',context)

def updateTask(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'task/update_task.html', context)

def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context={'item':item}
    return render(request,'task/delete.html', context)

def handleSignup(request):
    #get the post parameter
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # validation for creating the user 
        if len(username) > 15:
            messages.error(request, 'Your Username should be less than 15 charecters.')
            return redirect('/')
        
        #validation for alphanumeric
        if not username.isalnum():
            messages.error(request, 'Your Username should only contain letters and numbers.')
            return redirect('/')

        #to check weather username already exist or not
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already exist')
            return redirect('/')
        
        #to check weather email already exist or not
        if User.objects.filter(email=email).exists():
            messages.info(request,'email already exist')
            return redirect('/')

        # validation of confirming the password
        if pass1 != pass2:
            messages.error(request, 'Password do not matched.')
            return redirect('/')
        
        #creating the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your icoder account has been successfully created.')
        return redirect('/')
    else:
        HttpResponse('404-page not found')

def handleLogin(request):
    if request.method =='POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']

        user = authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request,'you have successfully logged In your account.')
            return redirect('/')

        else:
            messages.error(request,'Invalid credential. please try again.')
            return redirect('/')
    
    return HttpResponse('404-page not found')

def handleLogout(request):
    logout(request)
    messages.success(request,'you have successfully logged Out.')
    return redirect('/')

