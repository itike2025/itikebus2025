from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime
# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	email_confirmed = models.BooleanField(default=False)
	user_image = models.ImageField(default='prophile_photo/user_profile.png',upload_to="prophile_photo")
	birth_date = models.DateTimeField(null=True, blank=True)

	sex = models.CharField(choices=(
		('M',"Male"),
		('F',"Female")), 
	max_length= 1,default='')

	status = models.CharField(choices=(
		('S','Single'),
		('M','Married'),
		('D','Divoreced'),
		('Se','Separated')), 
		max_length=20, default='')


	def __str__(self):
		return f'{self.user.username} Profile'



		def save(self,*args, **kwargs):
			super().save()
			img = Image.open(self.image.path)
			if img.height > 300 or img.width>300:
				output_size = (300,300)
				img.thumbnail(output_size)
				img.save(self.image.path)



