"""python_exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from exam_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutV, name='logout'),
    path('courses/', views.list_courses, name='list_courses'),
    path('students/', views.list_students, name='list_students'),
    path('course/', views.add_course, name='add_course'),
    path('course/<int:course_id>', views.get_course, name='get_course'),
    path('edit_course/<int:course_id>', views.edit_course, name='edit_course'),
    path('destroy_course/<int:course_id>', views.destroy_course, name='destroy_course'),

    path('indeks/<int:student_id>', views.index, name='indeks'),
    path('add_subject/<int:subject_id>/<int:student_id>', views.add_subject_to_indeks, name='add_subject'),
    path('subject_passed/<int:subject_id>/<int:student_id>', views.subject_passed, name='subject_passed'),
    path('remove_subject/<int:subject_id>/<int:student_id>', views.remove_subject_from_indeks, name='remove_subject')
]
