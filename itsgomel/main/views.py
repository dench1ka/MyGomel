from django.shortcuts import render
from django.http import HttpResponse
from .models import Mural, Comment, MuralSuggestion, News, NewsImage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder
import json


def index(request):
    return render(request, 'main/index.html')


def mural(request):
    offset = int(request.GET.get('offset', 0))
    limit = 4

    # Для AJAX-запросов - возвращаем только часть данных
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        murals = Mural.objects.all()[offset:offset + limit]
        data = []
        for mural in murals:
            data.append({
                'id': mural.id,
                'title': mural.title,
                'address': mural.address,
                'image_url': mural.image.url,
            })
        return JsonResponse({'murals': data})

    # Для обычного запроса - все муралы для карты
    all_murals = Mural.objects.all()
    comments = Comment.objects.order_by('-created_at')[:10]

    # Подготовка данных для карты
    murals_coords = Mural.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    mural_data = [
        {
            'id': m.id,
            'title': m.title,
            'lat': m.latitude,
            'lng': m.longitude
        } for m in murals_coords
    ]

    context = {
        'murals': all_murals[:limit],
        'all_murals': all_murals,
        'initial_offset': limit,
        'comments': comments,
        'murals_json': json.dumps(mural_data, cls=DjangoJSONEncoder),
    }
    return render(request, 'mural/mural.html', context)

def get_embed_link(original_url):
    if not original_url:
        return None
    if "watch?v=" in original_url:
        return original_url.replace("watch?v=", "embed/")
    elif "youtu.be/" in original_url:
        video_id = original_url.split("/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return original_url

def mural_detail(request, pk):
    mural = get_object_or_404(Mural, pk=pk)
    embed_link = get_embed_link(mural.video_url)

    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')

        if name and text:
            Comment.objects.create(mural=mural, name=name, text=text)
            return redirect('mural_detail', pk=pk)

    comments = mural.comments.order_by('-created_at')

    # Подготовка данных для карты
    mural_data = {
        'id': mural.id,
        'title': mural.title,
        'lat': mural.latitude,
        'lng': mural.longitude,
        'address': mural.address
    }

    return render(request, 'mural/mural_detail.html', {
        'mural': mural,
        'video_url': embed_link,
        'comments': comments,
        'mural_json': json.dumps(mural_data, cls=DjangoJSONEncoder),
    })

def suggest_mural(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        if not all([name, email, address, description]):
            return JsonResponse({'status': 'error', 'message': 'Все поля, кроме файла, обязательны'}, status=400)

        MuralSuggestion.objects.create(
            name=name,
            email=email,
            address=address,
            description=description,
            file=file
        )
        return JsonResponse({'status': 'success', 'message': 'Предложение успешно отправлено'})

    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)

def news_list(request):
    news_list = News.objects.order_by('-date')
    return render(request, 'news/news.html', {'news_list': news_list})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})