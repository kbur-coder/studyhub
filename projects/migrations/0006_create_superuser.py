from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_profile'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]

