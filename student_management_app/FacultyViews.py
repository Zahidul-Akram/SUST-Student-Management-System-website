import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from student_management_app.models import Courses, SessionYear, Students, Faculties, StudentResult, CustomUser


def faculty_home(request):
    return render(request,"faculty_template/faculty_home_template.html")
def take_attendance(request):
    courses=Courses.objects.filter(faculty_id=request.user.id)
    session_years = SessionYear.objects.all()
    return render(request,"faculty_template/take_attendance_template.html",{"courses":courses,"session_years": session_years})


@csrf_exempt
def get_students(request):
    course_id=request.POST.get("course")
    session_year=request.POST.get("session_year")
    course=Courses.objects.get(id=course_id)
    session_model=SessionYear.objects.get(id=session_year)
    students=Students.objects.filter(department_id=course.department_id,session_year_id=session_model)
    list_data=[]
    for student in students:
        data_student={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name,"registration":student.registration}
        list_data.append(data_student)

    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)



def faculty_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    faculty = Faculties.objects.get(admin=user)

    return render(request, "faculty_template/faculty_profile_template.html",{"user": user, "faculty": faculty})

def faculty_add_result(request):
    courses=Courses.objects.filter(faculty_id=request.user.id)
    session_years=SessionYear.objects.all()
    return render(request,"faculty_template/faculty_add_result.html",{"courses":courses,"session_years":session_years})
def student_result_save(request):
    if request.method!='POST':
        return HttpResponseRedirect('Method Not Allowed')
    student_admin_id=request.POST.get('student_list')
    attendance_marks=request.POST.get('attendance_marks')
    semester_final_marks=request.POST.get('semester_final_marks')
    term_test_marks=request.POST.get('term_test_marks')
    grade = request.POST.get('grade')
    course_id=request.POST.get('course')
    student_obj=Students.objects.get(admin=student_admin_id)

    course_obj=Courses.objects.get(id=course_id)

    try:
        check_exist=StudentResult.objects.filter(course_id=course_obj,student_id=student_obj).exists()
        if check_exist:
            result=StudentResult.objects.get(course_id=course_obj,student_id=student_obj)
            result.course_semester_final_marks=semester_final_marks
            result.course_term_test_marks= term_test_marks
            result.course_attendance_marks= attendance_marks
            result.course_grade=grade
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect("/faculty_add_result")
        else:
            result=StudentResult(student_id=student_obj,course_id=course_obj,course_grade=grade,course_semester_final_marks=semester_final_marks,course_term_test_marks=term_test_marks,course_attendance_marks=attendance_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect("/faculty_add_result")
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect("/faculty_add_result")



