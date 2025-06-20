from rest_framework import serializers
from .models import User, Feedback

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

# Serializer for Feedback model
class FeedbackSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)  # nested manager info

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['manager']
