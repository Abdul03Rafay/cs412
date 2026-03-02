# File: mini_insta/models.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 2/20/2026.
# Description: Python file to define relevant models and their data attributes.

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulates the requirment fields for an profile.'''
    
    # data atributes of a profile:
    user_name = models.TextField(blank=False)
    display_name= models.TextField(blank=False)
    bio_text= models.TextField(blank=False)
    join_date= models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)
    
    def __str__(self):
        ''' Return a string representation on this Profile object.'''
        return f'{self.user_name} - {self.display_name}'
    
    def get_all_posts(self):
        '''Return all of the Posts related to this profile.'''
        
        posts = Post.objects.filter(profile=self)
        return posts
        
    def get_followers(self):
        '''Return a list of Profiles that follow this Profile.'''
        follows = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        '''Return the number of followers for this Profile.'''
        return len(self.get_followers())

    def get_following(self):
        '''Return a list of Profiles that this Profile follows.'''
        follows = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in follows]

    def get_num_following(self):
        '''Return the number of Profiles this Profile follows.'''
        return len(self.get_following())
        
    def get_post_feed(self):
        '''Return a list of Posts from all Profiles that this Profile follows.'''
        return Post.objects.filter(profile__in=self.get_following()).order_by('-timestamp')

    def get_absolute_url(self):
        '''Return the URL to redirect to after successfully updating profile.'''
        from django.urls import reverse
        return reverse('mini_insta:show_profile', kwargs={'pk': self.pk})
    
class Post(models.Model):
    '''Encapsulate the idea of Post with relevant data attributes.'''
    
    # data attributes of a Post:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=False)
    
    def __str__(self):
        '''Return a string representation of this post object.'''
        return f'{self.caption}'
    
    def get_all_photos(self):
        '''Return all of the Photos related to this post.'''
        
        photos = Photo.objects.filter(post=self)
        return photos

    def get_all_comments(self):
        '''Return all of the Comments related to this post.'''
        return Comment.objects.filter(post=self)

    def get_likes(self):
        '''Return all of the Likes related to this post.'''
        return Like.objects.filter(post=self)
    
class Photo(models.Model):
    '''Encapsuate the data attributes of Photo related to Post.'''
    
    # data attributes of a Photo:
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''Return a string representation of this photo object.'''
        if self.image_url:
            return f'{self.image_url}'
        elif self.image_file:
            return f'{self.image_file.url}'
        return f'Photo for post {self.post.pk}'

    def get_image_url(self):
        '''Return the URL of the image, preferring image_url, then image_file.'''
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        return ''

class Follow(models.Model):
    '''Encapsualte the idea of an edge connecting two Profiles.'''
    
    profile = models.ForeignKey("Profile", related_name="follower_profile", on_delete=models.CASCADE)
    follower_profile = models.ForeignKey("Profile", related_name="profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this follow relation.'''
        return f'{self.follower_profile.user_name} follows {self.profile.user_name}'

class Comment(models.Model):
    '''Encapsulate the idea of a profile commenting on a post.'''
    
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this comment.'''
        return f'{self.profile.user_name} commented on {self.post.pk}: {self.text[:20]}'

class Like(models.Model):
    '''Encapsulate the idea of a profile liking a post.'''
    
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this like.'''
        return f'{self.profile.user_name} liked {self.post.pk}'
    