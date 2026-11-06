from movies.models import Category

def AllCategories(request):
    categories=Category.objects.all()
    return dict(categories=categories)