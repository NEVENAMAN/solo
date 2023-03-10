# Generated by Django 2.2.4 on 2023-01-19 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appMain', '0005_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_context', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('send_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='message_send', to='appMain.User')),
                ('send_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages_recieve', to='appMain.User')),
            ],
        ),
    ]
