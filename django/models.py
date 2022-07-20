from django.db import connections
from django.db import models

# Create your models here.

class indicator_room(models.Model):   
    Month_name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Total = models.CharField(max_length=100)
    P1_P2 = models.CharField(max_length=100)
    P3_P4 = models.CharField(max_length=100)
    P1 = models.CharField(max_length=100)
    P2 = models.CharField(max_length=100)
    P3 = models.CharField(max_length=100)
    P4 = models.CharField(max_length=100)
    class Meta:
        db_table = "indicator_it_equipment_count_per_type_per_salle"