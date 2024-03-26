from django.db import migrations
from app.models import State

def populate_states(apps, schema_editor):
    states = [
        'Kerala',
    ]

    for state_name in states:
        State.objects.create(name=state_name)

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_states),
    ]
