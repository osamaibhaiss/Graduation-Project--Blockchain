# Generated by Django 5.1.2 on 2024-10-22 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('election_date', models.DateField()),
                ('election_id', models.AutoField(primary_key=True, serialize=False)),
                ('election_name', models.CharField(max_length=100)),
                ('election_start_time', models.TimeField()),
                ('election_end_time', models.TimeField()),
                ('city', models.CharField(default='', max_length=100)),
                ('seats', models.IntegerField(default=0, verbose_name='Number of Seats')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity_card_number', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('second_name', models.CharField(blank=True, max_length=50)),
                ('third_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField()),
                ('has_voted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=100)),
                ('group_description', models.TextField()),
                ('group_image', models.ImageField(blank=True, upload_to='group_images/')),
                ('elections', models.ManyToManyField(related_name='groups', to='voting.election')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_seats', models.IntegerField()),
                ('total_votes', models.IntegerField(default=0)),
                ('election', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='voting.election')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='voting.group')),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('voter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='voting.voter')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='voting.election')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='voting.group')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='accounts.profile')),
            ],
            options={
                'unique_together': {('voter', 'election')},
            },
        ),
    ]
