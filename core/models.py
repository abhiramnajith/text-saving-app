from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Class
class User(AbstractUser):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    class Meta:
       verbose_name= 'User'

#Abstract Class
class BaseClass(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active_status = models.BooleanField(default=True)

    class Meta:
        abstract = True

class  Tag(models.Model):
    title = models.CharField(max_length=80,unique=True)

    
    def __str__(self):
        return self.title
        
    class Meta:
       verbose_name = 'Tag' 

class Snippet(BaseClass):
    title = models.CharField(max_length=80)
    text =models.TextField()
    created_user = models.ForeignKey(User,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Snippet' 

