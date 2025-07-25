from django.db import models

# Create your models here.

class Mural(models.Model):
    title = models.CharField("Название", max_length= 200)
    address = models.CharField("Адрес", max_length= 300)
    description = models.CharField("Описание", max_length=500)
    image = models.ImageField("Главное изображение", upload_to='')
    video_url = models.URLField("Ссылка на видео", blank=True, null=True)

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