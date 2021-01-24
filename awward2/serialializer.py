from rest_framework import serializers
from .models import*

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model =Project
        fields = ('id', 'project_title', 'date_posted', 'description', 'project-link')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =Profile
        fields = ('id', 'user', 'imag', 'bio', 'contact')