from django.contrib import messages,auth

from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm, MovieForm
from .models import Movie, Category


# Create your views here.
def home(request):
    movie = Movie.objects.all()
    items_per_page = 6
    paginator = Paginator(movie, items_per_page)
    page = request.GET.get('page')

    try:
        movie = paginator.page(page)
    except PageNotAnInteger:
        movie = paginator.page(1)
    except EmptyPage:
        movie = paginator.page(paginator.num_pages)
    return render(request,'home.html',{'movie_list':movie})
def details(request,id):
    movies=Movie.objects.get(id=id)
    return render(request,'details.html',{'films':movies})


def add(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'You need to log in to add a movie.')
            return redirect('moviessapp:login')

        title = request.POST.get('title')
        poster = request.FILES.get('poster')
        description = request.POST.get('description',None)
        release_date = request.POST.get('release_date')
        actors = request.POST.get('actors')
        category = request.POST.get('category')
        trailer_link = request.POST.get('trailer_link')
        added_by = request.user
        try:
            category = Category.objects.get(id=category)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category.')
            return redirect('moviessapp:add')
        move = Movie(title=title,poster=poster,description=description,release_date=release_date,actors=actors,category=category,trailer_link=trailer_link, added_by=added_by)
        move.save()
        return redirect('/')
    categories = Category.objects.all()
    return render(request, 'add.html',{'categories':categories})

def updatemovie(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.user != movie.added_by:
        return render(request, 'notforupdate.html', {'message': 'You are not authorized to update this movie.'})
    forms = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    if forms.is_valid():
        forms.save()
        return redirect('/')

    return render(request, 'updatemovie.html', {'forms': forms})
def deletemovie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        if request.user == movie.added_by:
            movie.delete()
            return redirect('/')
        else:
            return render(request, 'notauthorized.html', {'message': 'You are not authorized to delete this movie.'})
    return render(request, 'deletemovie.html')

def category_movies(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    movies = Movie.objects.filter(category=category)
    return render(request, 'category_movies.html', {'category': category, 'movies': movies})
def register(request):

    if request.method=='POST':
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name=request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password again']
        if not username or not first_name or not last_name or not email or not password or not cpassword:
            messages.info(request, "Please fill in all the required fields.")
            return redirect('moviessapp:register')
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username already exists!")
                return redirect('moviessapp:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request," already have this email!")
                return redirect('moviessapp:register')
            else:
                use=User.objects.create_user(password=password,username=username,first_name=first_name,last_name=last_name,email=email)
                use.save()
                messages.success(request, "User created successfully..!!")
                return redirect('moviessapp:login')
        else:
            messages.info(request,"invalid password")
            return redirect('moviessapp:register')
        return redirect('/')
    return render(request,'register.html')

def login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, "invaild username or password !")
                return redirect('moviessapp:login')
        return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def userprofile(request):
    user_details = None

    if request.user.is_authenticated:
        user_details = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
    return render(request, 'userprofile.html', {'user_details': user_details})

def updateprofile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('moviessapp:userprofile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'updateprofile.html', {'form': form})
def deleteprofile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('/')
    return render(request, 'deleteprofile.html')

def searchresult(request):
    movies = None
    query = None
    try:
        if 'q' in request.GET:
            query = request.GET.get('q')
            movies = Movie.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    except Exception as e:
        print(f"Error in search_result view: {e}")
    return render(request, 'search.html', {'query': query, 'movies': movies})

def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if Category.objects.filter(name=category_name).exists():
            messages.error(request, 'Category already exists.')
            return redirect('moviessapp:addcategory')
        category = Category(name=category_name)
        category.save()
        return redirect('/')

    return render(request, 'addcategory.html')
