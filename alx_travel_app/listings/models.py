import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Listing(models.Model):
    """
    Model representing a property listing in the travel app.
    Equivalent to the Property table in the SQL schema.
    """
    property_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings',
        db_index=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'property'
        indexes = [
            models.Index(fields=['host'], name='idx_property_host'),
        ]

    def __str__(self):
        return f"{self.name} - {self.location}"


class Booking(models.Model):
    """
    Model representing a booking for a property listing.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    property = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_index=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_index=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking'
        indexes = [
            models.Index(fields=['property'], name='idx_booking_property'),
            models.Index(fields=['user'], name='idx_booking_user'),
        ]

    def __str__(self):
        return f"Booking {self.booking_id} - {self.property.name}"

    def clean(self):
        """Validate that end_date is after start_date"""
        from django.core.exceptions import ValidationError
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date.')


class Review(models.Model):
    """
    Model representing a review for a property listing.
    """
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    property = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
        indexes = [
            models.Index(fields=['property'], name='idx_review_property'),
            models.Index(fields=['user'], name='idx_review_user'),
        ]
        # Optionally prevent duplicate reviews from same user for same property
        unique_together = ['property', 'user']

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"