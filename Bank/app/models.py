from django.db import models

# Create your models here.
class Gender(models.Model):
    gender = models.CharField(max_length=7)
    
    def __str__(self):
         return self.gender 
class STATE(models.Model):
    state =models.CharField(max_length=15)
    
    def __str__(self):
        return self.state   
    
    
class Account(models.Model):
    name = models.CharField(max_length=32)
    mobile = models.PositiveBigIntegerField()
    account_number = models.PositiveBigIntegerField(auto_created=True, unique=True)
    email = models.EmailField(unique=True)
    aadhaar = models.PositiveIntegerField()
    father_name = models.CharField(max_length=100)
    dob = models.DateField()
    address = models.CharField(max_length=1000)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    balance = models.PositiveSmallIntegerField(default=500)
    pin =models.IntegerField(blank=True,default=0000)
    states =models.ForeignKey(STATE,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_pics")

    
    def save(self,*args,**kwargs):
        if not self.account_number:
            last_account=Account.objects.order_by('-account_number').first()
            if last_account:
                self.account_number=last_account.account_number+1
            else:
                self.account_number = 1234567890
        super().save(*args,**kwargs)