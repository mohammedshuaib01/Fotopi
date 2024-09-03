from django.shortcuts import render,redirect
from django.views.generic import View
from fotopiapp.forms import RegistrationForm,Loginform,UserProfileUpdateForm,PostUploadForm,CommentForm
from django.contrib.auth import authenticate,login,logout
from fotopiapp.models import Post,UserProfile,Comments
from django.contrib import messages
from django.utils.decorators import method_decorator
from  fotopiapp.decorator import signin_required
from django.views.decorators.cache import never_cache





decs=[signin_required,never_cache]
# Create your views here.

 
class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"registration.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("signin")
        
        return render(request,"registration.html",{"form":form})
    

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=Loginform()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname, password=pwd)

            if user_object:
                login(request,user_object)
                return redirect("home")
            return render(request,"login.html",{"form":form})


@method_decorator(decs,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"logged out of session")
        return redirect("signin")
    

@method_decorator(decs,name="dispatch")
class HomeView(View):
    def get(self,request,*args,**kwargs):
        qs=Post.objects.all().order_by("-created_date")
        qs_2=UserProfile.objects.get(user=request.user)
        return render(request,"home.html",{"data":qs,"data2":qs_2})


@method_decorator(decs,name="dispatch")
class UserProfileView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.get(user=request.user)
        qs_2=Post.objects.filter(user=request.user).order_by("-created_date")
        return render(request,"myprofile.html",{"data":qs,"data_2":qs_2})

@method_decorator(decs,name="dispatch")
class UserProfileUpdateView(View):
    def get(self,request,*args,**kwargs):
        user_profile=UserProfile.objects.get(user=request.user)
        # form=UserProfileUpdateForm(instance=qs)
        form=UserProfileUpdateForm(instance=user_profile)
        return render(request,"profile_update.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        qs=UserProfile.objects.get(user=request.user)
        form=UserProfileUpdateForm(request.POST,instance=qs,files=request.FILES)

        if form.is_valid():
            form.instance.name=request.user
            form.save()
            messages.success(request,"profile updated successfully")
            return redirect ('userprofile')
        
        return render(request,"profile_update.html",{"form":form})  
    

@method_decorator(decs,name="dispatch")    
class PostUploadView(View):

    def get(self,request,*args,**kwargs):
        form=PostUploadForm()
        return render(request,"post_upload.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=PostUploadForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request,"new post uploaded")
            return redirect("userprofile")
        return render(request,"post_upload.html",{"form":form})
    
    

@method_decorator(decs,name="dispatch")   
class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Post.objects.get(id=id)

        action = request.POST.get("action")
        if action == "like":
            post_object.liked_by.add(request.user)
        
        elif action == "unlike":
            post_object.liked_by.remove(request.user)

        return redirect("home")


@method_decorator(decs,name="dispatch")
class CommentCreateView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Post.objects.get(id=id)
        form=CommentForm()
        return render(request,"comment_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Post.objects.get(id=id)
        form=CommentForm(request.POST)
        form.instance.post=post_object
        form.instance.user=request.user                  
        if form.is_valid():
            form.save()
            messages.success(request,"you commented for this post!")
            return redirect("home")
        return render(request,"comment_add.html",{"form":form})
    
    
@method_decorator(decs,name="dispatch")
class CommentListView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Post.objects.get(id=id)
        qs=Comments.objects.filter(post=post_object)
        return render(request,"comment_list.html",{"data":qs})
    

    
@method_decorator(decs,name="dispatch")
class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user)
        return render(request,"profile_list.html",{"data":qs})



@method_decorator(decs,name="dispatch")
class FollowView(View):
     def post(self,request,*args,**kwargs):
          id=kwargs.get('pk')
          profile_object=UserProfile.objects.get(id=id)
          action=request.POST.get("action")
          if action=="follow":
               request.user.profile.following.add(profile_object)
          elif action=="unfollow":
               request.user.profile.following.remove(profile_object)     
          return redirect(request.META.get('HTTP_REFERER', 'profile-list'))
     

@method_decorator(decs,name="dispatch")     
class FollowersListView(View):
    def get(self,request,*args,**kwargs):
        profile_object=request.user.profile
        qs=profile_object.followed_by.all()
        return render(request,"followers_list.html",{"followers":qs})
    
    
@method_decorator(decs,name="dispatch")     
class FollowingListView(View):
    def get(self,request,*args,**kwargs):
        profile_object=request.user.profile
        qs=profile_object.following.all()
        return render(request,"following_list.html",{"following":qs})
    

    



    
        
        



