from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone 
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import datetime



# Create your models here.
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
def upload_location(instance, filename):
    #filebase, extension=filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    return "%s/%s" %(instance.id, filename)



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    image = models.ImageField( 
            upload_to=upload_location,
            null=True, 
            blank=True,
            width_field='width_field',
            height_field='height_field')
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    #content = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    #content2 = RichTextUploadingField(blank=True, null=True,config_name='special')

    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    

    objects = PostManager()
    

    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", args={str(self.id)})
    
    class Meta:
        ordering=["-timestamp", "-updated"]





class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    Date = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return "{post} - {user} - {Date}" .format(post=self.post, user=self.user.username, Date=self.Date)
        

class Author(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    mobile_no =models.CharField(max_length=13, blank=True)
    address =models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-details', args=(self.id))
    def __str__(self):
        return self.user.username


class Ratings(models.Model):
    no_of_ratings = models.IntegerField(default=0, null=True, blank=True)
    no_of_users = models.IntegerField(default=0, null=True, blank=True)
    average_rating = models.IntegerField(default=0, null=True, blank=True)
    voted_by = models.ManyToManyField(User, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title

