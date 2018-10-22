from django.db import models
from django.conf import settings

from .validators import validateDweet

def get_dummy_user(self):
        """
        this prevents deleting of comments in case user deletes the account. Placeholder for non-existent user
        """

        return get_user_model().objects.get_or_create(username='--deleted--')[0]

# Create your models here.
class Dweet(models.Model):
    """
    stores user dweet details in m2m fashion to avoid duplicates of retweet
    """    

    dweeted_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name ="dweets", through="DweetRelation")    
    dweet_text = models.TextField(max_length=240, blank = False, null = False, validators=[validateDweet])    

    def __str__(self):
        return self.dweet_text

class DweetRelation(models.Model):
    """
    This relationship table stores the details relation between Dweet and User 
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dweet = models.ForeignKey(Dweet, on_delete=models.CASCADE)
    dweet_created_at = models.DateTimeField(auto_now_add=True)
    dweet_last_updated =  models.DateTimeField(auto_now=True)
    #dweet_delete_marked = models.BooleanField(default=False)
    #dweet_dm_at = models.DateTimeField(null=True, blank=False)

    def __str__(self):
    	"""
    	string representation of the object to print
    	"""
        
    	return self.user.username +" -> " + self.dweet.dweet_text
    
class Comments(models.Model):
    """
    stores comments placed on the Dweets
    """

    commented_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_dummy_user), default=None)
    comment = models.TextField(max_length=240, blank = False, null = False, validators=[validateDweet])
    commented_at = models.DateTimeField(auto_now_add=True)
    dweet = models.ForeignKey(Dweet, related_name="comments", on_delete=models.CASCADE, blank=True, null=True)    
    
    def __str__(self):
        return self.comment


class Reaction(models.Model):
    """
    stores reactions to the original tweet
    """

    REACTION = (
        ('1','Like'),
        ('0','Dislike'),
        ('','')
        )

    reacted_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction = models.IntegerField(choices=REACTION, default=0)
    reacted_at = models.DateTimeField(auto_now_add=True)
    dweet = models.ForeignKey(Dweet, related_name="reactions", on_delete=models.CASCADE, blank=True, null=True)
