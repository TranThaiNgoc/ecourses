from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class ItemBase(models.Model):
    # bổ sung column kế thừa nhưng không tạo bản table kế thừa
    class Meta:
        abstract = True
    subject = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d')

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    def __str__(self):
        return self.name

class Course(ItemBase):
    class Meta:
        # unique column
        unique_together = ('subject', 'category')
        # quy định sắp xếp danh sách sắp xếp
        ordering = ['-id', 'created_date']
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

class Lesson(ItemBase):
    class Meta:
        unique_together = ('subject', 'courses')
    content = models.TextField()
    # 3 option
    # SET_NULL các records liên qua khi xóa sẽ là null luôn không xóa theo
    # SET_DEFAULT set khóa học theo mặc định khi xóa ForeignKey
    # CASCADE xóa khóa cha records con xóa theo
    # PROTECT khi còn records con thì khóa cha không được xóa
    courses = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name