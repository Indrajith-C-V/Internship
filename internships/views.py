from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Internship, Application, CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm, InternshipForm
from django.db.models import Count
from django.utils import timezone
def home(request):
    internships = Internship.objects.filter(deadline__gte=timezone.now()).order_by('-posted_at')

    if not request.user.is_authenticated:
        # Guests see carousel
        return render(request, 'home.html', {'guest_view': True})

    # Logged-in users see internship list
    return render(request, 'home.html', {
        'internships': internships,
        'is_authenticated': True
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Welcome back!')
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('home')
    return redirect('home')

@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if Application.objects.filter(user=request.user, internship=internship).exists():
        messages.info(request, 'You have already applied.')
        return redirect('home')

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        if resume:
            Application.objects.create(user=request.user, internship=internship, resume=resume)
            messages.success(request, 'Application submitted!')
            return redirect('my_applications')
        else:
            messages.error(request, 'Please upload your resume.')

    return render(request, 'apply.html', {'internship': internship})

@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('internship')
    return render(request, 'my_applications.html', {'applications': applications})

# Admin Views
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    users = CustomUser.objects.all()
    internships = Internship.objects.all()
    applications = Application.objects.all().select_related('user', 'internship')
    return render(request, 'admin_dashboard.html', {
        'users': users,
        'internships': internships,
        'applications': applications
    })


@login_required
def admin_users(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')

    users = CustomUser.objects.annotate(
        participation_count=Count('application')
    ).order_by('-date_joined')

    return render(request, 'admin_users.html', {
        'users': users,
        'total_users': users.count()
    })

@login_required
def admin_internships(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')

    internships = Internship.objects.all().order_by('-posted_at')

    return render(request, 'admin_internships.html', {
        'internships': internships,
        'total_internships': internships.count()
    })

@login_required
def admin_applications(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')

    applications = Application.objects.all().select_related('user', 'internship').order_by('-applied_at')

    return render(request, 'admin_applications.html', {
        'applications': applications,
        'total_applications': applications.count()
    })



@login_required
def internship_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Internship added.')
            return redirect('admin_dashboard')
    else:
        form = InternshipForm()
    return render(request, 'internship_form.html', {'form': form, 'title': 'Add Internship'})

@login_required
def internship_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, 'Internship updated.')
            return redirect('admin_dashboard')
    else:
        form = InternshipForm(instance=internship)
    return render(request, 'internship_form.html', {'form': form, 'title': 'Edit Internship'})

@login_required
def internship_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    internship = get_object_or_404(Internship, pk=pk)
    internship.delete()
    messages.success(request, 'Internship deleted.')
    return redirect('admin_dashboard')

@login_required
def user_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    user = get_object_or_404(CustomUser, pk=pk)
    if user == request.user:
        messages.error(request, 'Cannot delete own account.')
    else:
        user.delete()
        messages.success(request, 'User deleted.')
    return redirect('admin_dashboard')

@login_required
def application_approve(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    application = get_object_or_404(Application, pk=pk)
    application.status = 'Accepted'
    application.save()
    messages.success(request, 'Application accepted.')
    return redirect('admin_applications')

@login_required
def application_reject(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    application = get_object_or_404(Application, pk=pk)
    application.status = 'Rejected'
    application.save()
    messages.success(request, 'Application rejected.')
    return redirect('admin_applications')

@login_required
def admin_application_detail(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')

    application = get_object_or_404(Application.objects.select_related('user', 'internship'), pk=pk)
    return render(request, 'admin_application_detail.html', {'application': application})

@login_required
def admin_internship_detail(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')

    internship = get_object_or_404(Internship, pk=pk)
    applications = Application.objects.filter(internship=internship).select_related('user').order_by('-applied_at')
    return render(request, 'admin_internship_detail.html', {
        'internship': internship,
        'applications': applications,
        'total_applications': applications.count()
    })