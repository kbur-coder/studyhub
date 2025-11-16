from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе', max_length=500)
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Местоположение')
    website = models.URLField(blank=True, null=True, verbose_name='Веб-сайт')
    github = models.CharField(max_length=100, blank=True, null=True, verbose_name='GitHub')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Профиль {self.user.username}'
    
    def get_avatar_url(self):
        """Возвращает URL аватара или дефолтный"""
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает профиль автоматически при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    external_link = models.URLField(blank=True, null=True, verbose_name='Внешняя ссылка')
    technologies = models.CharField(max_length=200, verbose_name='Технологии')
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='Фотография')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', verbose_name='Автор', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

