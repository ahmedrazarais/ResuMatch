from django.db import models

# Create your models here.

# Create model only two rows text area for job ad and resume

class Raw_Data(models.Model):
    job_ad = models.TextField()
    resume = models.TextField()
    
    def __str__(self):
        return self.job_ad + " " + self.resume