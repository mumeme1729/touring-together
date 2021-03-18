from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid
import io
from django.core.files.base import File

def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])

def upload_plan_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['plan', str(instance.userPlan.id)+str(".")+str(ext)])
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    #ログインに使う物
    USERNAME_FIELD = 'email'

    def get_followers(self):
        relations = Relationship.objects.filter(follow=self)
        return [relation.follower for relation in relations]

    def __str__(self):
        return self.email


class Profile(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nickName = models.CharField(max_length=20)
    text=models.CharField(max_length=200,blank=True,null=True)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    base=models.CharField(blank=True,null=True,max_length=50)

    def __str__(self):
        return self.nickName

class Relationship(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    userFollow = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userFollow',on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following',blank=True,on_delete=models.CASCADE)


class Plan(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    destination = models.CharField(max_length=50,db_index=True)
    date=models.DateField()
    userPlan = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPlan',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    text=models.CharField(max_length=150,blank=True, null=True,)
    img = models.ImageField(blank=True, null=True, upload_to=upload_plan_path)

    def __str__(self):
        return self.destination


class Comment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE,related_name='plan')

    def __str__(self):
        return self.text

class Notification(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    status =models.BooleanField(default=True)
    receive=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receive',on_delete=models.CASCADE)
    send=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='send',on_delete=models.CASCADE)
    targetplan=models.ForeignKey(Plan, on_delete=models.CASCADE,related_name='targetplan',blank=True, null=True,)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receive
