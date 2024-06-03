from django.db import models
from account.models import SocialUser, UserProfile
from mimetypes import guess_type
# Create your models here.

  
def upload_post(instance, filename):
    return 'posts\{username}\{filename}'.format(username=instance.user.username,filename=filename)


class Post(models.Model):
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='post')
    content = models.FileField(upload_to='upload_post')
    caption = models.CharField(max_length=255, blank=True, null=True)
    post_created = models.DateTimeField(auto_now_add=True)
    post_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + "'s post ->" + str(self.pk)
    
    def media_type_html(self):
        type_tuple = guess_type(self.content.url, strict=True)
        if (type_tuple[0]).__contains__("image"):
            return "image"
        elif (type_tuple[0]).__contains__("video"):
            return "video"

