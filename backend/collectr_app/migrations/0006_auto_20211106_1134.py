# Generated by Django 3.2.8 on 2021-11-06 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectr_app', '0005_auto_20211104_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='cover_image',
            field=models.ImageField(upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='feedbackreviewrequest',
            name='evidence',
            field=models.ImageField(upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='cover_image',
            field=models.ImageField(upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='newcollectionrequest',
            name='evidence',
            field=models.ImageField(upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='newitemrequest',
            name='evidence',
            field=models.ImageField(upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='tradeattachment',
            name='attachment',
            field=models.FileField(upload_to='attachments/'),
        ),
        migrations.AddConstraint(
            model_name='reputationfeedback',
            constraint=models.UniqueConstraint(fields=('receiver', 'sender'), name='rate-limiting-feedbacks'),
        ),
    ]
