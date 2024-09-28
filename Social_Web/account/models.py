from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class SocialUserManager(BaseUserManager):
    def create_user(self, email, roll,username, password=None):
        
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an Username")
        if not roll:
            raise ValueError("Users must have an Roll")
        
        user = self.model(
            email=self.normalize_email(email),
            roll=roll,
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, roll,username, password=None):
        
        user = self.create_user(
            email,
            password=password,
            roll=roll,
            username = username
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class SocialUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    roll = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = SocialUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["roll", "username"]

    def __str__(self):
        return self.email
    
    def get_group_permissions(obj=None):
        return obj

   
def upload_profile_pic(instance, filename):
    return 'profile_pics\{username}\{filename}'.format(username=instance.user.username,filename=filename)

class UserProfile(models.Model):
    user = models.OneToOneField(SocialUser, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to=upload_profile_pic, default='default.jpg')
    bio = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
    

class Follow(models.Model):
    follower = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.follower.username) + ' follows ' + str(self.following.username)