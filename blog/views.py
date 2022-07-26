from tokenize import group
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm,  PostForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html', {'posts': posts})

def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/dashboard.html', {'posts': posts, 'full_name':full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login')


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')

    if request.method == "POST":
        fm = AuthenticationForm(request=request, data = request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(request, username = uname, password = upass)

            if user is not None:
                login(request, user)
                messages.success(request,'Logged in successfully !!')
                return HttpResponseRedirect('/dashboard/')
            else:
                fm = AuthenticationForm()    
                return render(request, 'blog/login.html', {'form': fm})
    else:
        fm = AuthenticationForm()
        return render(request, 'blog/login.html', {'form':fm})


def user_signup(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully!!')
            user = fm.save()
            group = Group.objects.get(name= 'Author')
            user.groups.add(group)
    else:
        fm = SignUpForm() 
    return render(request, 'blog/signup.html', {'form': fm})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# add Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title = title, desc = desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


#updade Post/Edit post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':  
            pi = Post.objects.get(pk = id)
            form = PostForm(request.POST, instance = pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk = id)
            form = PostForm(instance = pi)
        return render(request, 'blog/updatepost.html', {'form': form})                    
    else:
        return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk = id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login') 
