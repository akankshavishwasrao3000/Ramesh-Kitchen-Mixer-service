from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ramesh', '0010_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='ramesh.product',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='reserved_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
