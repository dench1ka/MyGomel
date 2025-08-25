import requests
from django.db import models

class Mural(models.Model):
    title = models.CharField("Название", max_length=200)
    address = models.CharField("Адрес", max_length=300)
    description = models.CharField("Описание", max_length=500)
    image = models.ImageField("Главное изображение", upload_to='')
    video_url = models.URLField("Ссылка на видео", blank=True, null=True)
    latitude = models.FloatField("Широта", blank=True, null=True)
    longitude = models.FloatField("Долгота", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Если координаты не указаны, пытаемся получить их по адресу
        if (self.latitude is None or self.longitude is None) and self.address:
            self.latitude, self.longitude = self.get_coords_from_address(self.address)
        super().save(*args, **kwargs)

    @staticmethod
    def get_coords_from_address(address):
        try:
            url = 'https://nominatim.openstreetmap.org/search'
            params = {
                'q': address,
                'format': 'json',
                'limit': 1,
                'addressdetails': 0,
            }
            headers = {'User-Agent': 'MyMuralApp/1.0 (your_email@example.com)'}  # важен User-Agent!

            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
        except Exception as e:
            print(f"Ошибка геокодирования: {e}")
        return None, None

    def __str__(self):
        return self.title

class Comment(models.Model):
    mural = models.ForeignKey(Mural, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"

class MuralSuggestion(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    address = models.CharField("Предлагаемый адрес", max_length=300)
    description = models.TextField("Описание мурала")
    file = models.FileField("Фото/Видео", upload_to='suggestions/', blank=True, null=True)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.address}"

class News(models.Model):
    title = models.CharField("Название новости", max_length=255)
    description = models.TextField("Описание новости")
    date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Изображение", upload_to="news_images/")

    def __str__(self):
        return f"Изображение для {self.news.title}"

class ImprovementGallery(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    before_image = models.ImageField(upload_to="gallery/before/")
    after_image = models.ImageField(upload_to="gallery/after/")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title