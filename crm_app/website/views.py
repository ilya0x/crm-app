from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecord
from .models import Record


def home(request):
    records = Record.objects.all()

    # Check to see if the user is logging in:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "Unable to login!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "Goodbye!")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def contact_record(request, pk):
    if request.user.is_authenticated:
        # Look up the Contact record
        contact_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'contact_record': contact_record})
    else:
        messages.success(request, "You must be logged in to view this page. ")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        _ = Record.objects.get(id=pk)
        _.delete()
        messages.success(request, "Contact Deleted!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do this!")
        return redirect('home')


def add_record(request):
    form = AddRecord(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Contact Added!")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to do this!")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecord(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to do this!")
        return redirect('home')
