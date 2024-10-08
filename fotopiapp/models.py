from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime
from django.utils import timezone
from django.db.models.signals import post_save



# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile" )
    address=models.CharField(max_length=200, null=True)
    phone=models.CharField(max_length=200, null=True)
    profil_pic=models.FileField(upload_to="profilepic", null=True, blank=True)
    dob=models.DateField(null=True)
    bio=models.CharField(max_length=200,null=True)
    following=models.ManyToManyField("self",related_name="followed_by",symmetrical=False, blank=True)
    block=models.ManyToManyField("self",related_name="blocked", symmetrical=False,blank=True)
    

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userpost")
    title=models.CharField(max_length=200,null=True)
    post_image=models.ImageField(upload_to="posters",null=True, blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="post_like")

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    user=models.ForeignKey(User,related_name="comment",on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post,related_name="post_comments",on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Strories(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userstory")
    title=models.CharField(max_length=200)  
    post_image=models.ImageField(upload_to="stories",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    expiry_date=models.DateTimeField()

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.expiry_date:
         self.expiry_date=timezone.now()+timezone.timedelta(days=1)

        super().save(*args,**kwargs)

def create_profile(sender,created,instance,**kwargs):
    
     if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)

   