from django.db import migrations
from app.models import District, State

def populate_districts(apps, schema_editor):
    states_and_districts = {
        "Kerala": [ "Alappuzha",
            "Ernakulam",
            "Idukki",
            "Kannur",
            "Kasaragod",
            "Kollam",
            "Kottayam",
            "Kozhikode",
            "Malappuram",
            "Palakkad",
            "Pathanamthitta",
            "Thiruvananthapuram",
            "Thrissur",
            "Wayanad"],
    }

    for state_name, districts in states_and_districts.items():
        state = State.objects.get(name=state_name)
        for district_name in districts:
            District.objects.create(name=district_name, state=state)

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20240324_1511'),
    ]

    operations = [
        migrations.RunPython(populate_districts),
    ]
