# Generated by Django 5.0.1 on 2024-02-04 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_medicament_pharmacien_commande_pharmacie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commande',
            old_name='produit',
            new_name='medicament',
        ),
    ]