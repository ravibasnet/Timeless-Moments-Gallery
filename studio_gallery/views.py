from django.shortcuts import render, get_object_or_404
from .models import Category, Photo
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def gallery_home(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    
    if selected_category:
        photos = Photo.objects.filter(category__slug=selected_category)
    else:
        photos = Photo.objects.all()
    
    # Convert to list of dictionaries with required fields
    photo_list = []
    for photo in photos:
        photo_list.append({
            'id': photo.id,
            'title': photo.title,
            'image': photo.image.url,
            'category__name': photo.category.name,
            'upload_date': photo.upload_date.isoformat(),  # Convert datetime to string
            'description': photo.description
        })
    
    context = {
        'categories': categories,
        'photos': photos,
        'photo_list_json': json.dumps(photo_list, cls=DjangoJSONEncoder),  # Use Django's JSON encoder
        'selected_category': selected_category
    }
    return render(request, 'studio_gallery/gallery_home.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    photos = category.photos.all()
    return render(request, 'studio_gallery/category.html', 
                 {'category': category, 'photos': photos})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'studio_gallery/photo_detail.html', 
                 {'photo': photo})
