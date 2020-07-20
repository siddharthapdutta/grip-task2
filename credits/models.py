from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Transfer(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    credits = models.IntegerField(default=0)