# dadjokes/migrations/0002_add_initial_data.py
# Data migration to seed initial Joke and Picture records.

from django.db import migrations

JOKES = [
    {"text": "Why don't scientists trust atoms? Because they make up everything!", "contributor": "Abdul Rafay"},
    {"text": "I'm reading a book about anti-gravity. It's impossible to put down.", "contributor": "Abdul Rafay"},
    {"text": "Why did the scarecrow win an award? Because he was outstanding in his field.", "contributor": "Abdul Rafay"},
    {"text": "What do you call fake spaghetti? An impasta!", "contributor": "Abdul Rafay"},
    {"text": "Why can't you give Elsa a balloon? Because she'll let it go.", "contributor": "Abdul Rafay"},
    {"text": "I would tell you a joke about construction, but I'm still working on it.", "contributor": "Abdul Rafay"},
    {"text": "What do you call cheese that isn't yours? Nacho cheese.", "contributor": "Abdul Rafay"},
]

PICTURES = [
    {"image_url": "https://media.giphy.com/media/d2lcHJTG5Tscg/giphy.gif", "contributor": "Abdul Rafay"},
    {"image_url": "https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif", "contributor": "Abdul Rafay"},
    {"image_url": "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif", "contributor": "Abdul Rafay"},
    {"image_url": "https://media.giphy.com/media/1gdiMjfHd1IpW/giphy.gif", "contributor": "Abdul Rafay"},
    {"image_url": "https://media.giphy.com/media/GeimqsH0TLDt4tScGw/giphy.gif", "contributor": "Abdul Rafay"},
    {"image_url": "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif", "contributor": "Abdul Rafay"},
]


def add_initial_data(apps, schema_editor):
    '''Insert initial Joke and Picture records.'''
    Joke = apps.get_model('dadjokes', 'Joke')
    Picture = apps.get_model('dadjokes', 'Picture')

    for joke_data in JOKES:
        Joke.objects.create(**joke_data)

    for picture_data in PICTURES:
        Picture.objects.create(**picture_data)


def remove_initial_data(apps, schema_editor):
    '''Remove all Joke and Picture records (reverse migration).'''
    Joke = apps.get_model('dadjokes', 'Joke')
    Picture = apps.get_model('dadjokes', 'Picture')
    Joke.objects.all().delete()
    Picture.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('dadjokes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
