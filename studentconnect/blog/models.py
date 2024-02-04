from django.db import models
from django.utils import timezone
from collegeadmin.models import CollegeDatabase
from superadmin.models import UserAccount
import re

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
    
class Comment(models.Model):
    """
    Class For Comments
    """
    content = models.TextField()
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.author}{self.date_commented}"

class Like(models.Model):
    """
    Class for likes
    """
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return  f"{self.user}{self.date_liked}"

class BlogPost(models.Model):   
    """
    Class for creating the blogposts
    """
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200,)
    content = models.TextField()
    image_url = models.URLField(blank=True,null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CollegeDatabase, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    likes = models.ManyToManyField(Like, blank=True)

    def save(self, *args, **kwargs):
        """
        if the content in the post containe any of the tags(sentences startign with the # value then the model
        instance for the blog post will crete the tags can use in future for refering
        """
        super().save(*args, **kwargs)

        # Extract sentences starting with a hash value from the content
        sentences = re.findall(r'#\w+', self.content)

        # Create tags for each extracted sentence
        for sentence in sentences:
            tag, created = Tag.objects.get_or_create(name=sentence[1:])
            self.tags.add(tag)

    def __str__(self):
        return self.title
    
