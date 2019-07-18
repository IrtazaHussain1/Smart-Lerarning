from django.db import models
from django.contrib.auth.models import User
from Login_app.choices import *


# Create your models here.
class Teacher(models.Model):
    t_teacher=models.ForeignKey(User, default=1 ,on_delete=models.CASCADE)
    t_gender=models.CharField(max_length=1, choices=gender_list)
    t_departmant=models.CharField(max_length=3, choices=department_list)
    def __str__(self):
        return self.t_teacher.first_name+" "+self.t_teacher.last_name
