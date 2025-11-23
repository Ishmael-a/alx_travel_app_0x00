# ALX Travel App - Database Modeling and Seeding

This project implements database models, serializers, and seeding functionality for a travel booking application built with Django and Django REST Framework.

## Project Structure

```
alx_travel_app_0x00/
└── alx_travel_app/
    └── listings/
        ├── models.py              # Database models
        ├── serializers.py         # DRF serializers
        └── management/
            └── commands/
                └── seed.py        # Database seeding command
```

## Models

### Listing (Property)
Represents a property available for booking.

**Fields:**
- `property_id` (UUID): Primary key
- `host` (ForeignKey): Reference to User model
- `name` (CharField): Property name (max 100 chars)
- `description` (TextField): Detailed description
- `location` (CharField): Property location (max 100 chars)
- `price_per_night` (DecimalField): Nightly rate
- `created_at` (DateTimeField): Auto-generated creation timestamp
- `updated_at` (DateTimeField): Auto-updated modification timestamp

### Booking
Represents a customer booking for a property.

**Fields:**
- `booking_id` (UUID): Primary key
- `property` (ForeignKey): Reference to Listing
- `user` (ForeignKey): Reference to User
- `start_date` (DateField): Check-in date
- `end_date` (DateField): Check-out date
- `total_price` (DecimalField): Total booking cost
- `status` (CharField): One of 'pending', 'confirmed', 'canceled'
- `created_at` (DateTimeField): Auto-generated creation timestamp

### Review
Represents a user review for a property.

**Fields:**
- `review_id` (UUID): Primary key
- `property` (ForeignKey): Reference to Listing
- `user` (ForeignKey): Reference to User
- `rating` (IntegerField): Rating from 1 to 5
- `comment` (TextField): Review text
- `created_at` (DateTimeField): Auto-generated creation timestamp

## Serializers

### ListingSerializer
Serializes Listing model data for API endpoints with nested host information.

### BookingSerializer
Serializes Booking model data with nested property and user details. Includes validation for date logic.

### ReviewSerializer
Serializes Review model data with nested property and user information. Validates rating range.

### Simplified Serializers
- `ListingListSerializer`: Lightweight version for list views
- `BookingListSerializer`: Lightweight version for booking lists

## Setup Instructions

### 1. Install Dependencies

```bash
pip install django djangorestframework
```

### 2. Create Migration Files

```bash
python manage.py makemigrations listings
```

### 3. Apply Migrations

```bash
python manage.py migrate
```

### 4. Seed the Database

Run the seeding command to populate with sample data:

```bash
python manage.py seed
```

To clear existing data before seeding:

```bash
python manage.py seed --clear
```

## Seed Command Features

The seeding command creates:
- **6 sample users** (3 hosts, 3 guests)
- **8 property listings** across various locations
- **15 bookings** with varied statuses
- **Multiple reviews** for select properties

### Sample Data Includes:
- Properties in Malibu, Aspen, New York, Tuscany, Bali, Boston, Lake Tahoe, and Scottsdale
- Bookings with realistic date ranges and pricing
- Reviews with ratings between 3-5 stars

## Database Indexes

The following indexes are automatically created for query optimization:
- `idx_property_host` on Listing.host
- `idx_booking_property` on Booking.property
- `idx_booking_user` on Booking.user
- `idx_review_property` on Review.property
- `idx_review_user` on Review.user

## Validation Rules

### Listing
- Price per night must be positive
- All required fields must be provided

### Booking
- End date must be after start date
- Start date cannot be in the past (for new bookings)
- Status must be one of: pending, confirmed, canceled

### Review
- Rating must be between 1 and 5
- One review per user per property (unique constraint)

## Testing the Setup

### Verify Models

```bash
python manage.py shell
```

```python
from listings.models import Listing, Booking, Review

# Check counts
print(f"Listings: {Listing.objects.count()}")
print(f"Bookings: {Booking.objects.count()}")
print(f"Reviews: {Review.objects.count()}")

# View a sample listing
listing = Listing.objects.first()
print(f"Property: {listing.name}")
print(f"Location: {listing.location}")
print(f"Price: ${listing.price_per_night}/night")
```

### Test Serializers

```python
from listings.serializers import ListingSerializer
from listings.models import Listing

listing = Listing.objects.first()
serializer = ListingSerializer(listing)
print(serializer.data)
```

## API Integration

These serializers are ready to be integrated with Django REST Framework views and viewsets:

```python
from rest_framework import viewsets
from listings.models import Listing, Booking
from listings.serializers import ListingSerializer, BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
```

## Key Features

✅ UUID primary keys for all models  
✅ Proper foreign key relationships with cascade deletion  
✅ Automatic timestamp tracking  
✅ Database indexes for performance  
✅ Comprehensive validation rules  
✅ DRF serializers with nested relationships  
✅ Management command for easy database seeding  
✅ Realistic sample data for development and testing

## Technologies Used

- **Django**: Backend framework
- **Django REST Framework**: API serialization
- **SQLite/PostgreSQL**: Database
- **Python**: Programming language

## Learning Outcomes

This project demonstrates:
- Defining Django models with relationships and constraints
- Creating DRF serializers for API data representation
- Implementing custom management commands
- Database seeding for development workflows
- Proper validation and data integrity practices

## Resources

- [Django Models Documentation](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django REST Framework Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Django Management Commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)
- [Django Relationships](https://docs.djangoproject.com/en/stable/topics/db/examples/)

## Author

ALX Travel App Development Team

## License

This project is created for educational purposes as part of the ALX Software Engineering program.