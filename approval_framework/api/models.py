from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=255)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Workflow(models.Model):
    workflow_id = models.AutoField(primary_key=True)
    workflow_name = models.CharField(max_length=255)
    trigger_value = models.DecimalField(max_digits=10, decimal_places=2)
    users_in_sequence = models.ManyToManyField(UserProfile)


class ApprovalRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    requested_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='approval_requests')
    approval_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Pending')
    workflow = models.ForeignKey(
        Workflow, on_delete=models.DO_NOTHING, related_name='approval_requests', default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

class ApprovalRecords(models.Model):
    approval = models.ForeignKey(ApprovalRequest, on_delete=models.DO_NOTHING,related_name='records')
    current_approver = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,related_name='approvals')
    status = models.CharField(max_length=20, default='Pending')
    order = models.IntegerField(null=True)

class ApprovalItems(models.Model):
    name = models.CharField(max_length=63)
    approval = models.ForeignKey(
        ApprovalRequest, on_delete=models.CASCADE, related_name="items")
    value = models.DecimalField(max_digits=10, decimal_places=2)


class Comments(models.Model):
    approval = models.ForeignKey(
        ApprovalRequest, on_delete=models.CASCADE, related_name="comments")
    line = models.CharField(max_length=200)
    headers = models.CharField(max_length=63)
