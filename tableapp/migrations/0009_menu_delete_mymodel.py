# Generated by Django 5.1.4 on 2024-12-11 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0008_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image_url', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('recommend', 'เมนูแนะนำ'), ('tomyam', 'ต้ม'), ('pad', 'ผัด'), ('kang', 'แกง'), ('tod', 'ทอด')], default='recommend', max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='MyModel',
        ),
    ]
