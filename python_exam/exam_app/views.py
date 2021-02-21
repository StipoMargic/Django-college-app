from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, PredmetForm, UpisiForm
from .models import Korisnik, Predmet, Upisi
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from operator import itemgetter


def home(request):
    most_popular_subject = {}
    if request.user.is_authenticated:
        enrollments = Upisi.objects.all()
        for enrollment in enrollments:
            name = Predmet.objects.filter(id=enrollment.predmet_id).first().ime
            if name in most_popular_subject:
                most_popular_subject[name] += 1
            else:
                most_popular_subject[name] = 1
        new_dic = {}
        sort = sorted(most_popular_subject.items(), key=itemgetter(1), reverse=False)
        for i in range(0, 3):
            new_dic[sort[i][0]] = sort[i][1]
        return render(request, 'index.html', {'enrolls': new_dic})

    return redirect('login')


def logoutV(request):
    logout(request)

    return render(request, 'logout.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        registrationForm = RegistrationForm()
        return render(request, 'registration.html', {'form': registrationForm})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'registration.html', {'form': form})

    return HttpResponseNotAllowed()


@login_required
def list_students(request):
    students = Korisnik.objects.all()

    return render(request, 'list_students.html', {'students': students})


@login_required
def list_courses(request):
    courses = Predmet.objects.all()
    return render(request, 'list_courses.html', {'courses': courses})


@login_required
def add_course(request):
    if request.method == 'GET':
        form = PredmetForm()
        return render(request, 'add_course.html', {'form': form})

    if request.method == 'POST':
        form = PredmetForm()
        if Predmet.objects.filter(ime=request.POST['ime']) or Predmet.objects.filter(kod=request.POST['kod']):
            messages.error('Predmet već postoji')

        if form.is_valid():
            form.save()
            return redirect('list_courses')

    return HttpResponseNotAllowed()


@login_required
def edit_course(request, course_id):
    course = Predmet.objects.filter(id=course_id).first()

    if request.method == 'GET':
        form = PredmetForm(instance=course)
        return render(request, 'edit_course.html', {'form': form})

    if request.method == 'POST':
        form = PredmetForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('list_courses')

    return HttpResponseNotAllowed()


@login_required
def get_course(request, course_id):
    course = Predmet.objects.filter(id=course_id)
    enrolls = Upisi.objects.filter(predmet_id=course_id).count()
    students = list(Korisnik.objects.filter(role='STUDENT'))
    enrolls_name = Upisi.objects.filter(predmet_id=course_id).values_list('student_id', flat=True)
    names = []

    for student in students:
        for name in enrolls_name:
            if student.id == name:
                names.append(student)

    return render(request, 'course.html', {'course': course, 'enrolls': enrolls, 'names': names})


@login_required
def destroy_course(request, course_id):
    course = Predmet.objects.get(id=course_id)
    course.delete()

    return redirect('list_courses')


@login_required
def index(request, student_id):
    subjects = Predmet.objects.all()
    student = Korisnik.objects.get(id=student_id)
    enrolled_subjects = Upisi.objects.filter(student_id=student.id)
    sub_id = Upisi.objects.filter(student_id=student.id).values_list('predmet', flat=True)
    not_enrolled = {}

    for subject in subjects:
        if subject.id not in sub_id:
            not_enrolled[subject.id] = subject.ime

    return render(request, 'indeks.html',
                  {'subjects': subjects, 'student': student,
                   'enrolled_subjects': enrolled_subjects, 'not_enrolled': not_enrolled})


def remove_subject_from_indeks(request, subject_id, student_id):
    entry = Upisi.objects.filter(student_id=student_id, predmet_id=subject_id)
    entry.delete()

    return redirect('indeks', student_id)


@login_required
def add_subject_to_indeks(request, subject_id, student_id):
    Upisi.objects.create(predmet_id=subject_id, student_id=student_id, status='NEPOLOZEN')

    return redirect('indeks', student_id)


@login_required
def subject_passed(request, subject_id, student_id):
    Upisi.objects.filter(predmet_id=subject_id, student_id=student_id).update(status='POLOZEN')

    return redirect('indeks', student_id)
