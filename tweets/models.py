
from django.conf import settings
from django.db import models
import random
from django.db.models import Q

User = settings.AUTH_USER_MODEL

# Create your models here.


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    likes = models.ForeignKey('Tweet', on_delete=models.CASCADE,)
    timestamp = models.DateTimeField(auto_now_add=True)


class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        # 'following' is relation MaToMa profile.follow->User
        profile_exist = user.following.exists()

        # qs list-append all userid i followed
        followed_users_id = []
        if profile_exist:
            # why use this list isn't modern
            # followed_users_id = list(user.following.all().values_list("user__id", flat=True))
            followed_users_id = user.following.all().values_list("user__id", flat=True)

        # qs filter all tweet with list user i followed, rm dup and sort
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")


class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)


class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    # null=True, on_delele=models.SETNULL # many users can many tweets
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tweets')
    likes = models.ManyToManyField(
        User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    # def __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None

    def serialize(self):
        '''
        Feel free to delete!
        '''
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
