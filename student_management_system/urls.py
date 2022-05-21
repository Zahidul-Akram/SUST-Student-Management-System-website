"""student_management_system URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from student_management_app import views, HodViews, FacultyViews, StudentViews
from student_management_system import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',views.showLoginpage,name="show_login"),
    path('get_user_details',views.GetUserDetails),
    path('logout_user',views.logout_user),
    path('dologin',views.dologin),
    path('admin_home',HodViews.admin_home),
    path('add_faculty',HodViews.add_faculty),
    path('add_faculty_save',HodViews.add_faculty_save),
    path('add_department',HodViews.add_department),
    path('add_department_save',HodViews.add_department_save),
    path('add_student',HodViews.add_student),
    path('add_student_save',HodViews.add_student_save),
    path('add_course',HodViews.add_course),
    path('add_course_save',HodViews.add_course_save),
    path('add_session_year',HodViews.add_session_year),
    path('add_session_year_save',HodViews.add_session_year_save),
    path('manage_faculty',HodViews.manage_faculty),
    path('manage_student',HodViews.manage_student),
    path('manage_department',HodViews.manage_department),
    path('manage_course',HodViews.manage_course),
    path('edit_faculty/<str:faculty_id>',HodViews.edit_faculty),
    path('edit_student/<str:student_id>',HodViews.edit_student),
    path('edit_department/<str:department_id>',HodViews.edit_department),
    path('edit_course/<str:course_id>',HodViews.edit_course),
    path('edit_faculty_save',HodViews.edit_faculty_save),
    path('edit_student_save',HodViews.edit_student_save),
    path('edit_department_save',HodViews.edit_department_save),
    path('edit_course_save',HodViews.edit_course_save),
    path('faculty_home',FacultyViews.faculty_home),
    path('student_home',StudentViews.student_home),

    path('get_students',FacultyViews.get_students),

    path('faculty_add_result',FacultyViews.faculty_add_result),
    path('student_result_save',FacultyViews.student_result_save),
    path('faculty_profile',FacultyViews.faculty_profile),
    path('student_profile',StudentViews.student_profile),
    path('view_result',StudentViews.student_view_result),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

