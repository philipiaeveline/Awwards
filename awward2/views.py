from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProjectSerializer,ProfileSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly




def index(request):
    projects = Project.get_projects()
    context={
        'projects' : projects,
    }
    return render(request,"index.html", context)

@login_required(login_url='/accounts/login/')
def project(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = ProjectForm(request.POST,request.FILES)
                if form.is_valid():
                    new_project = form.save(commit=False)
                    new_project.author = current_user
                    new_project.profile = profile
                    new_project.save()
                    return redirect('index')
            else:
                form = ProjectForm()
                
            context = {
                'user':current_user,
                'form':form
            }
            return render(request,'project.html', context)
    
@login_required(login_url='/accounts/login/')
def profile(request,profile_id):
    profile = Profile.objects.get(pk = profile_id)
    project = Project.objects.filter(profile_id=profile).all()
    
    context = {
        'profile':profile,
        'project':project
    }
    return render(request,"profile.html", context)
        
@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')

@login_required(login_url='/accounts/login/')
def new_profile(request):
    project = Project.objects.filter(author=request.user).order_by('-date_posted')
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Welcome into your account!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'project' : project
    }
    return render(request, 'profile/profile.html', context)

@login_required(login_url='/accounts/login/')
def project(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = ProjectForm(request.POST,request.FILES)
                if form.is_valid():
                    project = form.save(commit=False)
                    project.author = current_user
                    project.profile = profile
                    project.save()
                    return redirect('index')
            else:
                form = ProjectForm()
                
                context = {
                    'user':current_user,
                    'form':form
                }
            return render(request,'project.html', context)
        
# @login_required(login_url='/accounts/login/')
# @csrf_protect
# def rating(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     current_user = request.user
#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             design_rating = form.cleaned_data["design_rating"]
#             usability_rating = form.cleaned_data["usability_rating"]
#             content_rating = form.cleaned_data["content_rating"]
#             comment = form.cleaned_data["comment"]
#             rating = form.save(commit=False)
#             rating.project = project
#             rating.author = current_user
#             rating.design_rating = design_rating
#             rating.usability_rating = usability_rating
#             rating.content_rating = content_rating
#             rating.comment = comment
#             rating.save()

#     else:
#         form = RatingForm()
#     return render(request,'rating.html', {'project' : project, 'form' : form})   

class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_profile(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project= self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     


