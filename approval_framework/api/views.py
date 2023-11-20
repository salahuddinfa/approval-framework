from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserProfileSerializer, CompanySerializer, ApprovalRequestSerializer, CommentsSerializer, WorkflowSerializer
from .models import UserProfile, Company, ApprovalRequest, Workflow, Comments


class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class CompanyView(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class ApprovalRequestView(ModelViewSet):
    serializer_class = ApprovalRequestSerializer
    queryset = ApprovalRequest.objects.all()


class CommentsView(ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()


class WorkflowView():
    serializer_class = WorkflowSerializer
    queryset = Workflow.objects.all()

class ApprovalRejectionView(APIView):
    
    def patch(request,id):
        approval_request = get_object_or_404(id=id)
        data = request.data
        if 'status' not in data:
            return Response({'error': "include the status please"},status=status.HTTP_204_NO_CONTENT) 
        request_status = data['status']

        if request_status == 'Approved':
            serializer = ApprovalRequestSerializer(approval_request, data=data, partial=True)