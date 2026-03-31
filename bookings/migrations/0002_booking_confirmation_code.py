import bookings.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        # Step 1: add nullable (so existing rows don't conflict)
        migrations.AddField(
            model_name='booking',
            name='confirmation_code',
            field=models.CharField(max_length=8, null=True, editable=False),
        ),
        # Step 2: populate existing rows with unique codes
        migrations.RunSQL(
            sql="""
                UPDATE bookings_booking
                SET confirmation_code = upper(substr(hex(randomblob(4)), 1, 8))
                WHERE confirmation_code IS NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Step 3: enforce NOT NULL + UNIQUE
        migrations.AlterField(
            model_name='booking',
            name='confirmation_code',
            field=models.CharField(
                default=bookings.models._short_code,
                editable=False,
                max_length=8,
                unique=True,
            ),
        ),
    ]
