from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver



class Role(models.Model):
  '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  '''
  STUDENT = 1
  GUEST = 2
  EMPLOYEE = 3
  MANAGER = 4
  ADMIN = 5
  ROLE_CHOICES = (
      (STUDENT, 'student'),
      (GUEST, 'guest'),
      (EMPLOYEE, 'employee'),
      (MANAGER, 'manager'),
      (ADMIN, 'admin'),
  )

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()

class User(AbstractUser):
      roles = models.ManyToManyField(Role)

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='students')
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    reg_no=models.CharField(max_length=100)
    books_due=models.IntegerField(default=0)
    phone=models.CharField(max_length=15)

    def __str__(self):
        return self.fname


class Libman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='librarian')
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100,unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.fname

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    image=models.ImageField(upload_to='uploads/users/%Y%m%d/',default='uploads/users/default.jpg')
    email = models.EmailField(max_length=100)
    website=models.URLField(max_length=255,null=True,blank=True)
    biography=models.TextField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

