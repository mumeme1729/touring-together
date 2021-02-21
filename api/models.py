from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid

def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])
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
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName

class Relationship(models.Model):
    userFollow = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userFollow',on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following',blank=True,on_delete=models.CASCADE)


class Plan(models.Model):
    destination = models.CharField(max_length=50)
    date=models.DateField()
    userPlan = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPlan',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    text=models.CharField(max_length=150)

    def __str__(self):
        return self.destination


class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.text