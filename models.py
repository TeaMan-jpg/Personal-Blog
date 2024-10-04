from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Django():
#     def db(self):
#         data = self.model.objects.all()
#         return data


# class Home(ListView,Django):
#     model = Post

#     def __init__(str):
#         new = super().db()
#         print(new)

class Blog(models.Model):
    header = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        permissions = [('ban_user','can ban a user')]

    def __str__(self):
        return self.header


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default="default/image.png",upload_to="profile_pics/")
    
   

    
    bio = models.TextField()

    

    def __str__(self):
        return self.user.username
    

