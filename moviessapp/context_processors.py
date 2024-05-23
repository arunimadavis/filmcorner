from .models import Category

def categories(request):
    category_list = Category.objects.all()
    return {'category_list': category_list}