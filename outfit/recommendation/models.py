from django.db import models

class outfit(models.Model):
	username = models.CharField(max_length = 50)
	mobile_no = models.BigIntegerField()
	email = models.CharField(max_length = 30) 
	Password = models.CharField(max_length = 30)


class credentials(models.Model):
	username = models.CharField(max_length = 50)
	Password = models.CharField(max_length = 50)


class outfit_image(models.Model):
	User_Name = models.CharField(max_length=25)
	Top = models.ImageField(upload_to='outfit_images/', null = True)
	Bottom = models.ImageField(upload_to='outfit_images/', null = True)
	Dress = models.ImageField(upload_to='outfit_images/', null = True)
	Shoes = models.ImageField(upload_to='outfit_images/')
	Outerwear = models.ImageField(upload_to='outfit_images/', null = True)
	Purse = models.ImageField(upload_to='outfit_images/', null = True)
	Compatibility_Score = models.FloatField(null = True)