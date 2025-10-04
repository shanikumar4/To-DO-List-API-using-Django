from django.db import models
from django.contrib.auth.models import User
import datetime



class Todolist(models.Model):
    title = models.CharField(max_length=50)
    discription = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    up_date = models.DateTimeField(null= True, blank=True)
    del_date = models.DateTimeField(null= True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.title 

    


    
    