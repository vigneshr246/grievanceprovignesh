from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('staff', 'Staff'),
    ]


    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone",'name']


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class GrievanceCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


    def __str__(self):
        return self.name
   
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)


    def __str__(self):
        return self.name




class Grievance(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grievances")
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(GrievanceCategory, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="grievances")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_grievances")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title




class GrievanceAttachment(models.Model):
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to='grievance_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Attachment for {self.grievance.title}"


class Feedback(models.Model):
    grievance = models.OneToOneField(Grievance, on_delete=models.CASCADE, related_name="feedback")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Feedback for {self.grievance.title}"


class Report(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    grievance_count = models.IntegerField()
    resolved_count = models.IntegerField()
    escalated_count = models.IntegerField()
    average_resolution_time = models.DurationField()


    def __str__(self):
        return f"Report from {self.start_date} to {self.end_date}"
