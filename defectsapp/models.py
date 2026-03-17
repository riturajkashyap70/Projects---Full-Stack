from django.db import models
from django.contrib.auth.models import User

class defects_mod(models.Model):
   
  STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

  Defect_Id=models.CharField(max_length=10)
  Defect_Name=models.CharField(max_length=50)
  Assigned_By=models.ForeignKey(User,on_delete=models.CASCADE, related_name='assigned_by_defects')
  Assigned_To=models.ForeignKey(User,on_delete=models.CASCADE, related_name='assigned_to_defects')
  Assigned_Date=models.DateField(auto_now_add=True)
  Description=models.TextField()
  Defect_Status=models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
  Priority=models.CharField(max_length=20)
  
  def __str__(self):
   return self.Defect_Id+" "+str(self.Defect_Name)+" "+str(self.Assigned_Date) 
  
  
class developer(models.Model):
   dev_name=models.ForeignKey(User,on_delete=models.CASCADE)
   designation=models.CharField(max_length=50)
   experience=models.IntegerField()
   
class tester(models.Model):
   tester_name=models.ForeignKey(User,on_delete=models.CASCADE)
   designation=models.CharField(max_length=50)
   experience=models.IntegerField()
   is_admin=models.BooleanField(default=False)
   
class defect_screenshot(models.Model):
   defect=models.ForeignKey(defects_mod, on_delete=models.CASCADE)
   def_img=models.ImageField(upload_to='def_screenshot/',blank=True,null=True)

    
  
  

  
  
  
  