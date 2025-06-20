from rest_framework import  permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Feedback
from .serializers import UserSerializer, FeedbackSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status

# Filter to allow only managers
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'

# Filter to allow only employees
class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employee'

# 1. List all employees (for a manager)
class EmployeeListView(generics.ListAPIView):
    permission_classes = [IsManager]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(role='employee', manager=self.request.user)

# 2. Submit feedback to an employee
class FeedbackCreateView(generics.CreateAPIView):
    permission_classes = [IsManager]
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

# 3. List feedback for employee
class FeedbackReceivedListView(generics.ListAPIView):
    permission_classes = [IsEmployee]
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(employee=self.request.user)

# 4. Acknowledge feedback
class AcknowledgeFeedbackView(APIView):
    permission_classes = [IsEmployee]

    def post(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk, employee=request.user)
        feedback.acknowledged = True
        feedback.save()
        return Response({'status': 'Acknowledged'}, status=status.HTTP_200_OK)

class FeedbackUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_object(self):
        feedback = super().get_object()
        if feedback.manager != self.request.user:
            raise PermissionDenied("You can only edit your own feedback.")
        return feedback
    
@api_view(['POST'])
def mock_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)

from django.db.models import Count

class ManagerDashboardView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        team_members = User.objects.filter(manager=request.user)
        data = []

        for member in team_members:
            feedbacks = Feedback.objects.filter(employee=member)
            sentiment_count = feedbacks.values('sentiment').annotate(count=Count('id'))
            data.append({
                'employee': member.username,
                'feedback_count': feedbacks.count(),
                'sentiments': {item['sentiment']: item['count'] for item in sentiment_count}
            })

        return Response(data)

class EmployeeDashboardView(APIView):
    permission_classes = [IsEmployee]

    def get(self, request):
        feedbacks = Feedback.objects.filter(employee=request.user).order_by('-created_at')
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def mock_logout(request):
    if request.auth:
        request.auth.delete()
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')
