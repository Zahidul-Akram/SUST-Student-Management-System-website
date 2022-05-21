from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from student_management_app.models import CustomUser, Departments, Faculties, Courses, Students, SessionYear


def admin_home(request):
    return render(request,"hod_template/home_content.html")
def add_faculty(request):
    return render(request,"hod_template/add_faculty_template.html")

def add_faculty_save(request):
    if request.method !='POST':
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        address = request.POST.get("address")
        profile_pic = request.FILES.get("profile_pic")
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        contact_no=request.POST.get("contact_no")
        try:
            user=CustomUser.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,user_type=2)
            user.faculties.address=address
            user.faculties.profile_pic = profile_pic_url
            user.faculties.contact_no=contact_no
            user.save()
            messages.success(request,"Successfully Added Faculty")
            return HttpResponseRedirect("/add_faculty")
        except:
            messages.error(request,"Failed to Add Faculty")
            return HttpResponseRedirect("/add_faculty")


def add_department(request):
    return render(request,"hod_template/add_department_template.html")
def add_department_save(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        department=request.POST.get("department_name")
        try:
            department_model=Departments(department_name=department)
            department_model.save()
            messages.success(request,"Successfully Added Department")
            return HttpResponseRedirect("/add_department")
        except:
            messages.error(request,"Failed to Add Department")
            return HttpResponseRedirect("/add_department")


def add_student(request):
    departments=Departments.objects.all()
    sessions=SessionYear.objects.all()
    return render(request,"hod_template/add_student_template.html",{"departments":departments,"sessions":sessions})

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        registration=request.POST.get("registration")
        address = request.POST.get("address")
        session_year_id=request.POST.get("session")
        sex=request.POST.get("sex")
        department_id=request.POST.get("department")
        profile_pic = request.FILES.get('profile_pic')
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name, user_type=3)
            user.students.address = address
            user.students.registration=registration
            user.students.gender=sex
            department_obj=Departments.objects.get(id=department_id)
            user.students.department_id=department_obj
            user.students.profile_pic = profile_pic_url
            session_year_obj = SessionYear.objects.get(id=session_year_id)
            user.students.session_year_id=session_year_obj
            user.save()
            messages.success(request, "Successfully Added Student")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect("/add_student")
def add_course(request):
    departments=Departments.objects.all()
    faculties=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_course_template.html",{"departments":departments,"faculties":faculties})
def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        course_name = request.POST.get("course_name")
        department_id=request.POST.get("department")
        department=Departments.objects.get(id=department_id)
        faculty_id=request.POST.get("faculty")
        faculty=CustomUser.objects.get(id=faculty_id)
        try:
            course=Courses(course_name=course_name,department_id=department,faculty_id=faculty)
            course.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"Failed to Add Course")
            return HttpResponseRedirect("/add_course")
def manage_faculty(request):
    faculties=Faculties.objects.all()
    return render(request,"hod_template/manage_faculty_template.html",{"faculties":faculties})
def manage_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})
def manage_department(request):
    departments=Departments.objects.all()
    return render(request,"hod_template/manage_department_template.html",{"departments":departments})
def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})
def edit_faculty(request,faculty_id):
    faculty=Faculties.objects.get(admin=faculty_id)
    return render(request,"hod_template/edit_faculty_template.html",{"faculty":faculty})
def edit_faculty_save(request):
    if request.method !='POST':
        return HttpResponse("Method Not Allowed")
    else:
        faculty_id=request.POST.get("faculty_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        contact_no = request.POST.get("contact_no")
        # if request.FILES.get['profile_pic',False]:
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        # else:
        # profile_pic_url=None
        try:
            user=CustomUser.objects.get(id=faculty_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            faculty = Faculties.objects.get(admin=faculty_id)
            faculty.address=address
            faculty.contact_no=contact_no
            #if profile_pic_url != None:
            faculty.profile_pic = profile_pic_url
            faculty.save()
            messages.success(request,"Successfully Edited Faculty")
            return HttpResponseRedirect("/edit_faculty/"+faculty_id)
        except:
            messages.error(request,"Failed to Edit Faculty")
            return HttpResponseRedirect("/edit_faculty/"+faculty_id)
def edit_student(request,student_id):
    student=Students.objects.get(admin=student_id)
    departments=Departments.objects.all()
    sessions=SessionYear.objects.all()
    return render(request,"hod_template/edit_student_template.html",{"student":student , "departments":departments,"sessions":sessions})
def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id=request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        registration=request.POST.get("registration")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        session_year_id=request.POST.get("session")
        sex=request.POST.get("sex")
        department_id=request.POST.get("department")
        #if request.FILES.get['profile_pic',False]:
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        # else:
        #     profile_pic_url=None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name = last_name
            user.email=email
            user.username = username
            student=Students.objects.get(admin=student_id)
            student.address = address
            student.registration=registration
            student.gender=sex
            department_obj=Departments.objects.get(id=department_id)
            student.department_id=department_obj
            session_year_obj = SessionYear.objects.get(id=session_year_id)
            student.session_year_id =session_year_obj

            # if profile_pic_url != None:
            student.profile_pic = profile_pic_url
            student.save()
            messages.success(request, "Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/"+student_id)
        except:
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/"+student_id)
def edit_department(request,department_id):
    department=Departments.objects.get(id=department_id)
    return render(request,"hod_template/edit_department_template.html",{"department":department,"id":department_id})
def edit_department_save(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        department_id=request.POST.get("department_id")
        department_name=request.POST.get("department_name")
        try:
            department=Departments.objects.get(id=department_id)
            department.department_name=department_name
            department.save()
            messages.success(request,"Successfully Edited department")
            return HttpResponseRedirect("/edit_department/"+department_id)
        except:
            messages.error(request,"Failed to Edit Department")
            return HttpResponseRedirect("/edit_department/"+department_id)
def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    departments = Departments.objects.all()
    faculties = CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"departments":departments,"faculties":faculties,"id":course_id})
def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")
        department_id=request.POST.get("department")
        faculty_id=request.POST.get("faculty")

        try:
            faculty=CustomUser.objects.get(id=faculty_id)
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.faculty_id=faculty
            department=Departments.objects.get(id=department_id)
            course.department_id=department
            course.save()
            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect("/edit_course/"+course_id)
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect("/edit_course/"+course_id)
def add_session_year(request):
    return render(request,"hod_template/add_session_year_template.html")

def add_session_year_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method not Allowed")
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYear(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect("/add_session_year")
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect("/add_session_year")
