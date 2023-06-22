from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import MusicFile
from django.contrib.auth.forms import AuthenticationForm
from .forms import UploadFileForm
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    # Registration logic
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=email, email=email, password=password)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    # User login logic
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')


def upload_file(request):
    # File upload logic
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            visibility = form.cleaned_data['visibility']
            allowed_emails = form.cleaned_data['allowed_emails']
            
            # Get the uploader user instance
            uploader = User.objects.get(email=request.user.email)  # Convert to User instance
            
            # Create a new MusicFile instance
            MusicFile.objects.create(
                uploader=uploader,
                file=file,
                visibility=visibility,
                allowed_emails=allowed_emails
            )
            return redirect('homepage')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


@login_required
def homepage(request):
    # Homepage logic
    user = request.user
    public_files = MusicFile.objects.filter(visibility='public')
    private_files = MusicFile.objects.filter(visibility='private', uploader=user)
    protected_files = MusicFile.objects.filter(visibility='protected', allowed_emails__contains=user.email)
    files = public_files | private_files | protected_files
    return render(request, 'homepage.html', {'files': files})

@login_required
def user_logout(request):
    # User logout logic
    logout(request)
    return redirect('login')
