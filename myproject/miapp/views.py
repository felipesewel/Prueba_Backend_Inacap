from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from miapp.models import UserDetails
from .forms import LoginForm, CombinedUserEditForm, UserRegistrationForm
from django.contrib import messages

from .models import Book
from .forms import BookForm
from .models import Review
from .forms import ReviewForm


def login_view(request):
   if request.method == 'POST':
       form = LoginForm(request.POST)
       if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username, password=password)
           if user:
               login(request, user)
               return redirect('home')
           else:
               messages.error(request, 'Invalid username or password')
   else:
       form = LoginForm()
   return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
   logout(request)
   return redirect('login')

@login_required
def home(request):
   return render(request, 'home.html')

@login_required
def user_list(request):
   if request.user.userdetails.rol != 'admin':
       messages.error(request, 'You do not have permission to view this page')
       return redirect('home')
   users = User.objects.all()
   return render(request, 'user_list.html', {'users': users})

@login_required
def user_edit(request, user_id=None):
   if user_id:
       user = get_object_or_404(User, id=user_id)
       if request.user.userdetails.rol != 'admin' and request.user != user:
           messages.error(request, 'You do not have permission to edit this user')
           return redirect('home')
   else:
       user = request.user

   if request.method == 'POST':
       form = CombinedUserEditForm(request.POST, instance=user)
       if form.is_valid():
           form.save()
           messages.success(request, 'Profile updated successfully')
           return redirect('home')
   else:
       form = CombinedUserEditForm(instance=user)

   return render(request, 'user_edit.html', {'form': form})

@login_required
def user_delete(request, user_id):
   if request.user.userdetails.rol != 'admin':
       messages.error(request, 'You do not have permission to delete users')
       return redirect('home')

   user = get_object_or_404(User, id=user_id)
   if request.method == 'POST':
       user.delete()
       messages.success(request, 'User deleted successfully')
       return redirect('user_list')

   return render(request, 'user_delete.html', {'user': user})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Crear el usuario pero no lo guarda en la base de datos aún
            new_user = form.save(commit=False)
            # Establecer la contraseña
            new_user.set_password(form.cleaned_data['password'])
            # Guardar el usuario en la base de datos
            new_user.save()

            # Crear el detalle adicional del usuario
            UserDetails.objects.create(user=new_user)

            messages.success(request, 'El usuario se ha registrado exitosamente.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro creado exitosamente.')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

@login_required
def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro actualizado exitosamente.')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Libro eliminado exitosamente.')
        return redirect('book_list')
    return render(request, 'book_delete.html', {'book': book})

@login_required
def review_create(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    review = Review.objects.filter(book=book, user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Reseña guardada con éxito.')
            return redirect('book_list')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review_form.html', {'form': form, 'book': book})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Reseña eliminada con éxito.')
        return redirect('book_list')
    return render(request, 'review_confirm_delete.html', {'review': review})