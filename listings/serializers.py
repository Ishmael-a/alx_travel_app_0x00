from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):# type: ignore[misc]
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model.
    Includes nested host information and summary statistics.
    """
    host = UserSerializer(read_only=True)
    host_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='host',
        write_only=True
    )
    
    class Meta:
        model = Listing
        fields = [
            'property_id',
            'host',
            'host_id',
            'name',
            'description',
            'location',
            'price_per_night',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['property_id', 'created_at', 'updated_at']

    def validate_price_per_night(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than zero.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model.
    Includes nested property and user information.
    """
    property = ListingSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='property',
        write_only=True
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'property',
            'property_id',
            'user',
            'user_id',
            'start_date',
            'end_date',
            'total_price',
            'status',
            'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']

    def validate_booking(self, data):
        """
        Validate that:
        - end_date is after start_date
        - dates are not in the past
        """
        from django.utils import timezone
        
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError(
                    "End date must be after start date."
                )
            
            # Check if dates are in the past (only for new bookings)
            if not self.instance:
                today = timezone.now().date()
                if start_date < today:
                    raise serializers.ValidationError(
                        "Start date cannot be in the past."
                    )
        
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    Includes nested property and user information.
    """
    property = ListingSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='property',
        write_only=True
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = [
            'review_id',
            'property',
            'property_id',
            'user',
            'user_id',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['review_id', 'created_at']

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


# Simplified serializers for listing views
class ListingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing in list views"""
    host_name = serializers.CharField(source='host.username', read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'property_id',
            'name',
            'location',
            'price_per_night',
            'host_name'
        ]


class BookingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for bookings in list views"""
    property_name = serializers.CharField(source='property.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'property_name',
            'user_name',
            'start_date',
            'end_date',
            'status',
            'total_price'
        ]