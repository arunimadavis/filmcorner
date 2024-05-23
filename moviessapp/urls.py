
from django.urls import path
from . import views
app_name='moviessapp'
urlpatterns = [
    path('search/',views.searchresult,name='searchresult'),
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('movie/<int:id>/',views.details,name='details'),
    path('add/',views.add,name='add'),
    path('logout/',views.logout,name='logout'),
    path('category_movies/<int:category_id>/', views.category_movies, name='category_movies'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('deleteprofile/',views.deleteprofile,name='deleteprofile'),
    path('deletemovie/<int:movie_id>/', views.deletemovie, name='deletemovie'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('updatemovie//<int:id>/',views.updatemovie,name='updatemovie')


]