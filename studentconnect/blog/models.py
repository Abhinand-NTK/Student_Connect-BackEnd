from django.db import models
from django.utils import timezone
from collegeadmin.models import CollegeDatabase

# Create your models here.


class Tag(models.Model):
    """
    Class Tag is for Creating the tag for the blog posts
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    """
    Class for creating the author for a post
    """
    name = models.CharField(max_length=200)
    bio = models.TextField()

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """
    Class for creating the blogposts
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CollegeDatabase, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title