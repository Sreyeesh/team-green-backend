"""
Seed the database with demo data for the hackathon.

Usage:
    python manage.py seed
    python manage.py seed --flush   # wipes existing data first
"""
import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shops.models import Shop, Barber, Service
from bookings.models import Booking


SHOP_HOURS = {
    'mon': {'open': '09:00', 'close': '18:00'},
    'tue': {'open': '09:00', 'close': '18:00'},
    'wed': {'open': '09:00', 'close': '18:00'},
    'thu': {'open': '09:00', 'close': '18:00'},
    'fri': {'open': '09:00', 'close': '19:00'},
    'sat': {'open': '10:00', 'close': '17:00'},
    'sun': {'open': None, 'close': None},  # closed
}


class Command(BaseCommand):
    help = 'Seed the database with demo barbershop data'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Delete existing seed data first')

    def handle(self, *args, **options):
        if options['flush']:
            Booking.objects.all().delete()
            Service.objects.all().delete()
            Barber.objects.all().delete()
            Shop.objects.all().delete()
            User.objects.filter(username='owner@freshcuts.com').delete()
            self.stdout.write(self.style.WARNING('Flushed existing data.'))

        # ── Owner ─────────────────────────────────────────────────────────────
        owner, _ = User.objects.get_or_create(
            username='owner@freshcuts.com',
            defaults={'email': 'owner@freshcuts.com'},
        )
        owner.set_password('hackathon123')
        owner.save()

        # ── Shop ──────────────────────────────────────────────────────────────
        shop, _ = Shop.objects.get_or_create(
            slug='fresh-cuts',
            defaults={
                'owner': owner,
                'name': 'Fresh Cuts Barbershop',
                'description': 'Premium cuts and grooming in the heart of the city.',
                'logo_url': 'https://placehold.co/200x200?text=FreshCuts',
                'address': '42 Main Street, Downtown',
                'phone': '+1 555 010 0100',
                'hours': SHOP_HOURS,
            },
        )

        # ── Barbers ───────────────────────────────────────────────────────────
        marcus, _ = Barber.objects.get_or_create(
            shop=shop, name='Marcus Reid',
            defaults={
                'photo_url': 'https://placehold.co/300x300?text=Marcus',
                'bio': '10+ years of precision fades and classic cuts.',
                'specialties': ['Fade', 'Beard Trim', 'Hot Towel Shave'],
            },
        )
        priya, _ = Barber.objects.get_or_create(
            shop=shop, name='Priya Nair',
            defaults={
                'photo_url': 'https://placehold.co/300x300?text=Priya',
                'bio': 'Specialist in textured hair and modern styles.',
                'specialties': ['Textured Cuts', 'Colour', 'Kids Cuts'],
            },
        )

        # ── Services ──────────────────────────────────────────────────────────
        haircut, _ = Service.objects.get_or_create(
            shop=shop, name='Classic Haircut',
            defaults={'description': 'Scissor or clipper cut with finish.', 'duration_minutes': 30, 'price': '25.00', 'category': 'Hair'},
        )
        fade, _ = Service.objects.get_or_create(
            shop=shop, name='Skin Fade',
            defaults={'description': 'Zero to length fade with clean neckline.', 'duration_minutes': 45, 'price': '35.00', 'category': 'Hair'},
        )
        beard, _ = Service.objects.get_or_create(
            shop=shop, name='Beard Trim & Shape',
            defaults={'description': 'Full beard sculpt and hot towel finish.', 'duration_minutes': 30, 'price': '20.00', 'category': 'Beard'},
        )
        combo, _ = Service.objects.get_or_create(
            shop=shop, name='Cut & Beard Combo',
            defaults={'description': 'Haircut plus full beard service.', 'duration_minutes': 60, 'price': '50.00', 'category': 'Combo'},
        )

        # ── Bookings ──────────────────────────────────────────────────────────
        today = timezone.now().date()
        tomorrow = today + datetime.timedelta(days=1)

        def dt(date, hour, minute=0):
            return timezone.make_aware(datetime.datetime.combine(date, datetime.time(hour, minute)))

        bookings = [
            dict(
                shop=shop, barber=marcus, service=fade,
                datetime=dt(tomorrow, 10),
                duration_minutes=fade.duration_minutes,
                customer_name='Alex Johnson', customer_email='alex@example.com',
                customer_phone='+1 555 100 0001', status=Booking.STATUS_CONFIRMED,
            ),
            dict(
                shop=shop, barber=priya, service=haircut,
                datetime=dt(tomorrow, 11),
                duration_minutes=haircut.duration_minutes,
                customer_name='Sam Rivera', customer_email='sam@example.com',
                customer_phone='+1 555 100 0002', status=Booking.STATUS_PENDING,
            ),
            dict(
                shop=shop, barber=marcus, service=combo,
                datetime=dt(tomorrow, 14),
                duration_minutes=combo.duration_minutes,
                customer_name='Jordan Lee', customer_email='jordan@example.com',
                customer_phone='+1 555 100 0003', status=Booking.STATUS_PENDING,
            ),
        ]

        for b in bookings:
            Booking.objects.get_or_create(
                shop=b['shop'], barber=b['barber'], datetime=b['datetime'],
                defaults=b,
            )

        self.stdout.write(self.style.SUCCESS(
            '\nSeed complete!\n'
            f'  Shop slug : fresh-cuts\n'
            f'  Admin login: owner@freshcuts.com / hackathon123\n'
            f'  Barbers   : Marcus Reid, Priya Nair\n'
            f'  Services  : {haircut.name}, {fade.name}, {beard.name}, {combo.name}\n'
            f'  Bookings  : 3 (for tomorrow)\n'
        ))
