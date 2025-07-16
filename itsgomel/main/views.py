from django.shortcuts import render
from django.http import HttpResponse
from .models import Mural
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

    context = {
        'murals': murals,
        'initial_offset': limit,
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

    return render(request, 'mural/mural_detail.html', {
        'mural': mural,
        'video_url': embed_link
    })


