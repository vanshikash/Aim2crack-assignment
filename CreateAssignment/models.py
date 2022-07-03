from os import link
from django.db import models
import random
from django.contrib.auth.models import User
from django.db.models.fields import CharField, EmailField, TextField
from django.urls import reverse
    
class createlink(models.Model):
    link=models.CharField(max_length=12)
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=50)
    course_name = models.CharField(max_length=50)
    start = models.DateTimeField()
    no_of_submissions= models.IntegerField()
    perc_penalty= models.IntegerField()
    first_sub_time = models.DateTimeField()
    second_sub_time = models.DateTimeField()
    notif= models.CharField(max_length=12)
    neg_mark=models.CharField(max_length=12)
    face_rec=models.CharField(max_length=12)
    res_anno=models.CharField(max_length=100)
    result_time = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('CreateAssignment-home')


class Instruction(models.Model):
    assignment = models.OneToOneField(createlink,on_delete =models.CASCADE)
    instructions = models.TextField(max_length=500, blank= True)

    def get_absolute_url(self):
        return reverse('CreateAssignment-instructions')

    



