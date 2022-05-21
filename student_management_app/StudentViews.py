from django.shortcuts import render

from student_management_app.models import Students, StudentResult, CustomUser


def student_home(request):
    return render(request,"student_template/student_home_template.html")

def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    return render(request, "student_template/student_profile_template.html",{"user": user, "student": student})
def student_view_result(request):
    student=Students.objects.get(admin=request.user.id)
    student_results=StudentResult.objects.filter(student_id=student.id)
    return render(request,"student_template/student_view_result_template.html",{"student_results":student_results})