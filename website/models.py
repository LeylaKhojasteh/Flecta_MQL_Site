from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    project_type = models.CharField( max_length=100,blank=True )
    platform = models.CharField(max_length=100,blank=True)
    subject = models.CharField(max_length=250,blank=True,null=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
    def __str__(self):
      return  self.name
    

