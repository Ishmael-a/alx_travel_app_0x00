from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from alx_travel_app.listings.models import Listing, Booking, Review
from decimal import Decimal
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

        self.stdout.write('Starting database seeding...')

        # Create sample users (hosts and guests)
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))

        # Create sample listings
        listings = self.create_listings(users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(listings)} listings'))

        # Create sample bookings
        bookings = self.create_bookings(listings, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(bookings)} bookings'))

        # Create sample reviews
        reviews = self.create_reviews(listings, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(reviews)} reviews'))

        self.stdout.write(self.style.SUCCESS('\n✨ Database seeding completed successfully!'))

    def create_users(self):
        """Create sample users"""
        users_data = [
            {'username': 'john_host', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_host', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_guest', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Johnson'},
            {'username': 'sarah_guest', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Williams'},
            {'username': 'david_host', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Brown'},
            {'username': 'emma_guest', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Davis'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        return users

    def create_listings(self, users):
        """Create sample property listings"""
        listings_data = [
            {
                'name': 'Cozy Beach House',
                'description': 'Beautiful beachfront property with stunning ocean views. Perfect for families and couples seeking a relaxing getaway.',
                'location': 'Malibu, California',
                'price_per_night': Decimal('250.00'),
            },
            {
                'name': 'Mountain Retreat Cabin',
                'description': 'Secluded cabin in the mountains with hiking trails nearby. Ideal for nature lovers and adventure seekers.',
                'location': 'Aspen, Colorado',
                'price_per_night': Decimal('180.00'),
            },
            {
                'name': 'Downtown Luxury Apartment',
                'description': 'Modern apartment in the heart of the city with all amenities. Walking distance to restaurants, shops, and entertainment.',
                'location': 'New York, NY',
                'price_per_night': Decimal('300.00'),
            },
            {
                'name': 'Countryside Villa',
                'description': 'Spacious villa surrounded by vineyards and rolling hills. Features a private pool and outdoor dining area.',
                'location': 'Tuscany, Italy',
                'price_per_night': Decimal('450.00'),
            },
            {
                'name': 'Tropical Paradise Bungalow',
                'description': 'Charming bungalow steps from pristine beaches. Includes hammocks, outdoor shower, and tropical garden.',
                'location': 'Bali, Indonesia',
                'price_per_night': Decimal('120.00'),
            },
            {
                'name': 'Historic City Loft',
                'description': 'Renovated loft in a historic building with exposed brick and high ceilings. Perfect for urban explorers.',
                'location': 'Boston, Massachusetts',
                'price_per_night': Decimal('220.00'),
            },
            {
                'name': 'Lakefront Cottage',
                'description': 'Peaceful cottage on a private lake with dock and kayaks included. Great for fishing and water activities.',
                'location': 'Lake Tahoe, Nevada',
                'price_per_night': Decimal('195.00'),
            },
            {
                'name': 'Desert Oasis Villa',
                'description': 'Stunning modern villa with infinity pool overlooking desert landscape. Solar-powered and eco-friendly.',
                'location': 'Scottsdale, Arizona',
                'price_per_night': Decimal('350.00'),
            },
        ]

        listings = []
        hosts = [user for user in users if 'host' in user.username]
        
        for i, listing_data in enumerate(listings_data):
            listing = Listing.objects.create(
                host=hosts[i % len(hosts)],
                **listing_data
            )
            listings.append(listing)

        return listings

    def create_bookings(self, listings, users):
        """Create sample bookings"""
        bookings = []
        guests = [user for user in users if 'guest' in user.username]
        statuses = ['pending', 'confirmed', 'confirmed', 'confirmed', 'canceled']

        for i in range(15):
            listing = random.choice(listings)
            guest = random.choice(guests)
            
            # Generate random dates
            start_offset = random.randint(-30, 60)
            duration = random.randint(2, 14)
            start_date = datetime.now().date() + timedelta(days=start_offset)
            end_date = start_date + timedelta(days=duration)
            
            # Calculate total price
            total_price = listing.price_per_night * duration

            booking = Booking.objects.create(
                property=listing,
                user=guest,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=random.choice(statuses)
            )
            bookings.append(booking)

        return bookings

    def create_reviews(self, listings, users):
        """Create sample reviews"""
        reviews = []
        guests = [user for user in users if 'guest' in user.username]
        
        review_comments = [
            "Amazing place! Highly recommended for anyone visiting the area.",
            "Great location and very clean. The host was very responsive.",
            "Beautiful property with stunning views. Would definitely stay again.",
            "Good value for money. Some minor issues but overall satisfied.",
            "Exactly as described. Perfect for our family vacation.",
            "Outstanding experience. The property exceeded our expectations.",
            "Nice place but could use some updates. Still enjoyable though.",
            "Wonderful stay! The amenities were top-notch.",
            "Very comfortable and well-maintained. Great communication with host.",
            "Decent property but not quite what we expected from the photos.",
        ]

        # Create 1-3 reviews for random listings
        for listing in random.sample(listings, min(6, len(listings))):
            num_reviews = random.randint(1, 3)
            review_guests = random.sample(guests, min(num_reviews, len(guests)))
            
            for guest in review_guests:
                review = Review.objects.create(
                    property=listing,
                    user=guest,
                    rating=random.randint(3, 5),
                    comment=random.choice(review_comments)
                )
                reviews.append(review)

        return reviews