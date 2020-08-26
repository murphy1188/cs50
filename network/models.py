from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')

    serialize=True

    def __unicode__(self):
        return self.name

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
    from_person = models.ForeignKey(User, on_delete=models.PROTECT, related_name='from_people')
    to_person = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES, null=True, blank=True)

    
    def serialize(self):
        return {
            "id": self.id,
            #"follower": self.from_person,
            "follower": User.from_people,
            "following": self.to_person,
            "status": self.status
        }

class Comment(models.Model):
    commenter = models.ForeignKey("User", on_delete=models.CASCADE, related_name="commenter")
    timestamp = models.DateTimeField(auto_now_add=True)
    commentText = models.TextField(blank=True)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True)
    likers = models.ManyToManyField(User, blank=True, related_name="likes")
    comments = models.ManyToManyField(Comment, blank=True, related_name="postcomments")

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.user.username,
            "post": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likers": [user.username for user in self.likers.all()],
            "comments": [
                {
                    "commenter": comment.commenter.username,
                    "comment": comment.commentText,
                    "timestamp": comment.timestamp.strftime("%b %d %Y, %I:%M %p"),
                }
                 for comment in self.comments.all()],
        }
 

