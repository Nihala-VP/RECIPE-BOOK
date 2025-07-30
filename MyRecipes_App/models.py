from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):

    title=models.CharField(max_length=200)

    description=models.TextField()

    ingredients=models.TextField()

    instructions=models.TextField()

    cook_time=models.PositiveIntegerField()

    is_vegetarian=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.title



