from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User, Permission,Group
from django.contrib.contenttypes.models import ContentType
from .models import Blog, Profile
from .forms import LoginForm,RegisterForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.

def logins(req):
    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']
        user = User.objects.get(username=username)

        if not user.has_perm("personalblog.view_blog"):
            messages.success(req,"You are banned")
            return redirect("/blog/login/")


        user = authenticate(username=username,password=password)

        if user is not None:
           
            messages.success(req,"Login Successful")
            if User.objects.filter(pk=user.id, groups__name='Moderator').exists():
                print("Mod")
                print(user.user_permissions.all())
                login(req,user)
            else:
                print("Not Mod")
                print(user.user_permissions.all())
                login(req,user)
            return redirect("/blog/posts/")
        else:
            messages.error(req,"Login Failed!")


    return render(req,"personalblog/login.html/",{})


def signUp(req):

    
    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']
        email = req.POST['email']
        form = RegisterForm(req.POST)


        if (username and email and password):
            if User.objects.filter(username=username).exists():
                 messages.error(req,"User already exists")
                 return redirect("/blog/posts/")

            user = User.objects.create_user(username=username,password=password,email=email)


            contentType = ContentType.objects.get_for_model(Blog)

            permissions = Permission.objects.filter(content_type=contentType)
            print(permissions)

            for perm in permissions:
                user.user_permissions.add(perm)


            




            user.save()
            users = authenticate(username=username,password=password)

            if users is not None:
                messages.success(req,"Login Successful")
                myGroup = Group.objects.get(name="User")
                myGroup.user_set.add(user) 
                login(req,user)
                return redirect("/blog/posts/")
            
            else:
                messages.error(req,"Login Failed!")
    else:
        form = RegisterForm()

    return render(req,"personalblog/signUp.html",{"form":form})

@login_required(login_url="/blog/login/")
@permission_required("personalblog.view_blog", login_url='/blog/login/')
@permission_required("personalblog.change_blog", login_url='/blog/login/')
def showPosts(req):
    if not req.user.is_authenticated:
        print("frgegre")

    blogs = Blog.objects.all()

    if req.method == "POST":
        heading = req.POST["heading"]
        print(heading)
        text = req.POST["text"]

        if heading and text:
            b = Blog(author=req.user,header=heading,text=text)
            b.save()




    return render(req,"personalblog/posts.html",{"blogs":blogs})
            
@login_required(login_url="/blog/login/")
def showProfile(req,username):
    user = get_object_or_404(User,username=username)
    profile = get_object_or_404(Profile,user=user)

    userBlogs = Blog.objects.filter(author=user)

    return render(req,"personalblog/profile.html",{"userBlogs":userBlogs,"user":user,"profile":profile})



@login_required(login_url="/blog/login/")

def editProfile(req):
    userForm = UpdateUserForm(instance=req.user)
    profileForm = UpdateProfileForm(instance=req.user.profile)
    if req.method == "POST":
        userForm = UpdateUserForm(req.POST or None,instance=req.user)
        profileForm = UpdateProfileForm(req.POST or None,req.FILES,instance=req.user.profile)
    
        

        if userForm.is_valid() and profileForm.is_valid():
       
            userForm.save()
            profileForm.save()
            login(req,req.user)
            return redirect("/blog/posts/")
        else:
            userForm = UpdateUserForm(instance=req.user)
            profileForm = UpdateProfileForm(instance=req.user.profile)

    
    
    return render(req,"personalblog/editProfile.html",{"form":userForm,"profileForm":profileForm})


@login_required(login_url="/blog/login/")

def logouts(req):
    if (req.method == "POST"):
        logout(req)
        return redirect("/blog/login/")
    
    return render(req,"personalblog/logout.html",{})

@login_required(login_url="/blog/login/")
def editPosts(req,blogId):
    blog = Blog.objects.get(id=blogId)
    if req.method == "POST":
        heading = req.POST['heading']
        text = req.POST['text']

        if heading and text:
            
            blog.text = text
            blog.header = heading
            blog.save()
            return redirect("/blog/posts/")
        
    return render(req,"personalblog/editPost.html",{"blog":blog})

@login_required(login_url="/blog/login/")
@permission_required("personalblog.ban_user", login_url='/blog/login/')
def banUser(req,userId):
    blogs = Blog.objects.all()
    
    if req.method == "POST":
   
        try:
            user = get_object_or_404(User, id=userId)
            if (user.groups.filter(name="User").exists()):
               
    
    # Clear all user-specific permissions
                user.user_permissions.clear()

                group = Group.objects.get(name="User")
                user.groups.remove(group)
                groupBanned = Group.objects.get(name="Banned")
                user.groups.add(groupBanned)

            return redirect("/blog/users/")
        except User.DoesNotExist:
            return HttpResponse(status=404)
    else:
        user = get_object_or_404(User, id=userId)
        blogs = Blog.objects.all()
    return render(req,"personalblog/changePermission.html",{"blogs":blogs,"user":user})
        
@login_required(login_url="/blog/login/")
@permission_required("personalblog.ban_user", login_url='/blog/login/')
def displayUsers(req):

        users = User.objects.all()
        return render(req,"personalblog/displayUsers.html",{"users":users})


                
                