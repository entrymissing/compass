from django.db import models


class Goal(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  status = models.CharField(max_length=10,
                            choices=[('active', 'Active'),
                                     ('completed', 'Completed'),
                                     ('postponed', 'Postponed'),
                                     ('archived', 'Archived')])
  priority = models.IntegerField()
  context = models.CharField(max_length=10,
                             choices=[('work', 'Work'),
                                      ('private', 'Private')])
  goal_type = models.CharField(max_length=10,
                               choices=[('weekly', 'Weekly'),
                                        ('quarterly', 'Quarterly')])

  def __str__(self):
    return self.title


class Meditation(models.Model):
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=500)

  def __str__(self):
    return self.title
