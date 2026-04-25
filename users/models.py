from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Username must be set'))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        (True, _('Active')),
        (False, _('Inactive')),
    ] 
    STAFF_CHOICES = [
        (True, _('Yes')),
        (False, _('No')),
    ]
    user_creator = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='created_users',
      
    )
    username = models.CharField(max_length=30, unique=True)
    mobile_number = models.CharField(max_length=11, null=True, blank=True)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='custom_users')

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(choices=STATUS_CHOICES, default=True)
    
    email = models.EmailField(null=True, blank=True)
    picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.TextField() 
    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

