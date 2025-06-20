from django.urls import path
from .views import (
    home,
    EmployeeListView,
    FeedbackCreateView,
    FeedbackReceivedListView,
    AcknowledgeFeedbackView,
    FeedbackUpdateView,
    mock_login,
    mock_logout,
    ManagerDashboardView,
    EmployeeDashboardView
)

urlpatterns = [
    path('', home, name='home'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('feedback/create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback/received/', FeedbackReceivedListView.as_view(), name='feedback-received'),
    path('feedback/acknowledge/<int:pk>/', AcknowledgeFeedbackView.as_view(), name='feedback-acknowledge'),
    path('feedback/update/<int:pk>/', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('login/', mock_login, name='mock-login'),
    path('logout/', mock_logout, name='mock-logout'),
    path('dashboard/manager/', ManagerDashboardView.as_view(), name='dashboard-manager'),
    path('dashboard/employee/', EmployeeDashboardView.as_view(), name='dashboard-employee'),
]
