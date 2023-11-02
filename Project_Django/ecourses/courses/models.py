from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class Category (models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)


class ItemBase(models.Model):
    # Meta options này sẽ biến class này thành 1 class trừu tượng
    # khi tạo csdl nó sẽ không tạo class này thành 1 table
    class Meta:
        abstract = True

    subject = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)  # auto_now_add=True - Chỉ tạo khi Course được tạo
    update_date = models.DateTimeField(auto_now=True)  # auto_now=True - Cứ cập nhật Course thì update_date cũng update
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject


class Course (ItemBase):
    # 'subject', 'category' - 2 giá trị này gộp lại phải là unique
    # Trong 1 category không được trùng trên course
    class Meta:
        unique_together = ('subject', 'category')
        ordering = ["id"]

    description = models.TextField(null=True, blank=True)
    # on_delete = models.CASCADE - Khi xóa Category thì Course cũng bị xóa theo
    # on_delete = models.PROTECT - Khi Category đã có Course thì không cho xóa
    # on_delete = models.SET_DEFAULT - Khi Category bị xóa thì cái Course bị set về Category mặc định
    # on_delete = models.SET_NULL - Khi Category bị xóa thì cái Course bị set thành NULL
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  # Set khóa ngoại


class Lesson(ItemBase):
    class Meta:
        unique_together = ('subject', 'course')

    content = RichTextField()
    # on_delete = models.CASCADE - Khi xóa Category thì Course cũng bị xóa theo
    # on_delete = models.PROTECT - Khi Category đã có Course thì không cho xóa
    # on_delete = models.SET_DEFAULT - Khi Category bị xóa thì cái Course bị set về Category mặc định
    # on_delete = models.SET_NULL - Khi Category bị xóa thì cái Course bị set thành NULL
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)  # Set khóa ngoại
    tags = models.ManyToManyField('Tag', related_name="lessons", blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
