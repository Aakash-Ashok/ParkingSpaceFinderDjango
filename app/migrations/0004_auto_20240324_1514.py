from django.db import migrations
from app.models import District, State, Location

def populate_districts(apps, schema_editor):
    kerala = State.objects.get(name='Kerala')
    
    # Add locations for Ernakulam district
    ernakulam = District.objects.get(name='Ernakulam', state=kerala)
    ernakulam_locations = ['Kakkanad', 'Kaloor', 'Edappaly', 'Aluva', 'JNL', 'Fort Kochi']
    for location_name in ernakulam_locations:
        Location.objects.create(name=location_name, district=ernakulam)
    

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20240324_1513'),
    ]

    operations = [
        migrations.RunPython(populate_districts),
    ]
