from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    read_access = models.ManyToManyField(User, related_name='readable_posts')
    write_access = models.ManyToManyField(User, related_name='writeable_posts')
    public = models.BooleanField(default=True) # whether this post is visible to everyone
