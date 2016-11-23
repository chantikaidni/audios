from django.db import models
from django.contrib.auth.models import User
import uuid
import os, datetime
# Create your models here.


def get_file_path(instance, filename):
    # ext = filename.split('.')[-1]
    filename = "%s" % (uuid.uuid4())
    return os.path.join('static/recordings', filename)


class user_details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    profile_link = models.URLField(default='/welcome_user')
    dob = models.DateField(null=True)
    photo_link = models.URLField(default='/static/sitewide/anonymous-male.png')
    followers_total = models.IntegerField(default=0)
    circle_total = models.IntegerField(default=0)
    following_total = models.IntegerField(default=0)
    audios_total = models.IntegerField(default=0)
    intro = models.CharField(max_length=200,null=True)
    asked_total = models.IntegerField(default=0)
    answered_total = models.IntegerField(default=0)
    def __str__(self):
        return 'User_details: ' + self.full_name

class Recording(models.Model):
    # title = models.CharField(max_length=200)
    # user (User foreign key)
    # time (more precise than the date, which is already stored)
    # after (recursive foreign key)
    # convo (Conversation foreign key)

    # Managing Files: docs.djangoproject.com/en/1.6/topics/files/
    #
    # By default, Django stores files locally, using the MEDIA_ROOT and MEDIA_URL settings.
    #
    # When you use a FileField (or ImageField), Django provides
    # a set of APIs you can use to deal with that file.
    #
    #               TODO like what?
    #
    user = models.ForeignKey(User)
    view = models.CharField(max_length=8)
    audiolink = models.FileField(upload_to=get_file_path)
    

    likes_total = models.IntegerField(default=0)
    comments_total = models.IntegerField(default=0)
    shares_total = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True,null=True)
    title = models.CharField(max_length=70,default='Sample_audio')
    description = models.TextField(null=True)

    def __unicode__(self):
        return unicode(self.audiolink)

    def is_from_today(self):
        path_comp = self.audiolink._get_path().split('/')
        date_path = path_comp[-4:-1]  # Y/m/d
        date_comp = map(int, date_path)
        file_date = date(*date_comp)
        return file_date == date.today()

# class followers(models.Model):
class company(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)

class edu_insti(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)

class profession(models.Model):
    name = models.CharField(max_length=30)
    total = models.PositiveSmallIntegerField(default=0)

class user_work(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(company)
    profession = models.ForeignKey(profession)
    rank = models.PositiveSmallIntegerField(default=1)

class user_edu(models.Model):
    user = models.ForeignKey(User)
    edu_insti = models.ForeignKey(edu_insti)
    rank = models.PositiveSmallIntegerField(default=1)

class followers(models.Model):
    class Meta:
        unique_together = (('user', 'follower'),)
    user = models.ForeignKey(User)
    follower = models.ForeignKey(User,related_name='follower')
    date_time = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return 'Follower of : ' + self.user.first_name