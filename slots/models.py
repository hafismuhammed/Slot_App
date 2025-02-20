from django.db import models


class Slot(models.Model):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('interviewer', 'Interviewer'),
    )
    
    user_id = models.IntegerField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f'{self.user_id} - {self.role} - {self.date} - {self.start_time} - {self.end_time}'
    

