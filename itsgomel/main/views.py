from django.shortcuts import render
from django.http import HttpResponse
from .models import Mural, Comment, MuralSuggestion
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect


def index(request):
    return render(request, 'main/index.html')

def mural(request):
    offset = int(request.GET.get('offset', 0))
    limit = 4
    murals = Mural.objects.all()[offset:offset + limit]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for mural in murals:
            data.append({
                'id': mural.id,
                'title': mural.title,
                'address': mural.address,
                'image_url': mural.image.url,
            })
        return JsonResponse({'murals': data})

    comments = Comment.objects.order_by('-created_at')[:10]

    context = {
        'murals': murals,
        'initial_offset': limit,
        'comments': comments,
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
            return redirect('mural_detail', pk=pk)  # после сохранения - обновить страницу

    comments = mural.comments.order_by('-created_at')  # комментарии для этого мурала

    return render(request, 'mural/mural_detail.html', {
        'mural': mural,
        'video_url': embed_link,
        'comments': comments,
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