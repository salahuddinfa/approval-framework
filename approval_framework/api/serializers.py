from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Company, UserProfile, ApprovalRequest, Workflow, Comments


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'

class ApprovalRequestSerializer(serializers.ModelSerializer):
    requested_by = UserProfileSerializer()
    value = serializers.SerializerMethodField()

    def get_value(self,instance):
        value = instance.items.aggregate(value=Sum('value'))['value']
        if value is not None:
            return float(value)
        return 0
    
    class Meta:
        model = ApprovalRequest
        fields = '__all__'

class WorkflowSerializer(serializers.ModelSerializer):
    users_in_sequence = UserProfileSerializer(many=True)

    class Meta:
        model = Workflow
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    approval = ApprovalRequestSerializer()

    class Meta:
        model = Comments
        fields = '__all__'