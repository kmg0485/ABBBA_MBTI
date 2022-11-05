from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# 이미지 최적화
from image_optimizer.fields import OptimizedImageField


class UserManager(BaseUserManager):
    def create_user(self, nickname, password=None):
        if not nickname:
            raise ValueError('Users must have a nickname')

        user = self.model(
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None):
        user = self.create_user(
            nickname,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    nickname = models.CharField(
        verbose_name='nickname',
        max_length=20,
        unique=True,
    )
    email = models.EmailField(max_length=255, default='', blank=True)
    profile_img = OptimizedImageField(
        upload_to="uploads/%Y/%m/%d",
        optimized_image_output_size=(300, 300),
        optimized_image_resize_method="cover",  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
        null=True, blank=True
    )
    bio = models.CharField(max_length=255, default='', blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    mbti = models.CharField(max_length=4, default='', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin