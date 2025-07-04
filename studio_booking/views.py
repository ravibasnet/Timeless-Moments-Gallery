from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import BookingSession, AvailableSlot
from .serializers import BookingSessionSerializer, AvailableSlotSerializer
import json
from django.utils import timezone
import logging
from datetime import datetime
import os
from django.conf import settings

logger = logging.getLogger(__name__)

def booking_spa(request):
    """Main SPA view for booking system"""
    return render(request, 'studio_booking/spa.html')

@require_http_methods(["GET"])
def get_available_slots(request):
    """API endpoint to get available booking slots"""
    try:
        slots = AvailableSlot.objects.filter(date__gte=timezone.now().date())
        serializer = AvailableSlotSerializer(slots, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        logger.error(f"Error fetching available slots: {str(e)}")
        return JsonResponse({'error': 'Failed to fetch available slots'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_book_session(request):
    """API endpoint to create a new booking session"""
    logger.info('Booking API called')
    
    try:
        # Parse JSON data
        try:
            data = json.loads(request.body)
            logger.info(f'Received booking data: {data}')
        except json.JSONDecodeError as e:
            logger.error(f'JSON decode error: {str(e)}')
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid JSON data'
            }, status=400)
        
        # Validate required fields
        required_fields = ['client_name', 'client_email', 'client_phone', 
                          'session_type', 'duration', 'location', 'dates']
        
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            logger.error(f'Missing required fields: {missing_fields}')
            return JsonResponse({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'errors': {field: ['This field is required.'] for field in missing_fields}
            }, status=400)
        
        # Validate dates
        dates = data.get('dates', [])
        if not dates or not isinstance(dates, list):
            logger.error('No dates provided or dates is not a list')
            return JsonResponse({
                'status': 'error',
                'message': 'At least one date must be selected',
                'errors': {'dates': ['At least one date must be selected.']}
            }, status=400)
        
        # Validate date format
        try:
            for date_str in dates:
                datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError as e:
            logger.error(f'Invalid date format: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD.',
                'errors': {'dates': ['Invalid date format. Use YYYY-MM-DD.']}
            }, status=400)
        
        # Get or create default client
        try:
            client_id = data.get('client', 1)
            client = User.objects.get(id=client_id)
            logger.info(f'Using client: {client}')
        except User.DoesNotExist:
            # Create a default user if none exists
            try:
                client = User.objects.first()
                if not client:
                    client = User.objects.create_user(
                        username='default_client',
                        email='default@example.com',
                        first_name='Default',
                        last_name='Client'
                    )
                    logger.info(f'Created default client: {client}')
                data['client'] = client.id
            except Exception as e:
                logger.error(f'Error creating default client: {str(e)}')
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to create client account'
                }, status=500)
        
        # Validate duration
        try:
            duration = int(data['duration'])
            if duration < 1 or duration > 8:
                raise ValueError('Duration must be between 1 and 8 hours')
            data['duration'] = duration
        except (ValueError, TypeError) as e:
            logger.error(f'Invalid duration: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': 'Duration must be a number between 1 and 8',
                'errors': {'duration': ['Duration must be a number between 1 and 8.']}
            }, status=400)
        
        # Create booking using serializer
        serializer = BookingSessionSerializer(data=data)
        if serializer.is_valid():
            try:
                booking = serializer.save()
                logger.info(f'Booking created successfully: {booking.id}')
                
                # Return success response
                return JsonResponse({
                    'status': 'success',
                    'message': 'Booking created successfully',
                    'booking_id': booking.id,
                    'booking_ref': f'TM-{booking.id:06d}'
                })
                
            except Exception as e:
                logger.error(f'Error saving booking: {str(e)}', exc_info=True)
                return JsonResponse({
                    'status': 'error',
                    'message': f'Failed to save booking: {str(e)}'
                }, status=500)
        else:
            # Log detailed validation errors
            logger.error(f'Serializer validation errors: {serializer.errors}')
            
            # Format errors for response
            error_details = {}
            for field, errors in serializer.errors.items():
                error_details[field] = [str(error) for error in errors]
            
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid booking data',
                'errors': error_details
            }, status=400)
            
    except Exception as e:
        logger.exception('Unhandled exception in api_book_session')
        return JsonResponse({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def get_bookings(request):
    """API endpoint to get bookings"""
    logger.debug('Bookings API called')
    
    try:
        # Get query parameters
        status_filter = request.GET.get('status', 'completed')
        limit = request.GET.get('limit')
        
        # Build queryset
        queryset = BookingSession.objects.filter(status=status_filter).order_by('-created_at')
        logger.debug(f'Found {queryset.count()} {status_filter} bookings')
        
        # Apply limit if specified
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                logger.warning(f'Invalid limit value: {limit}')
        
        # Format bookings data
        bookings = []
        for booking in queryset:
            booking_data = {
                'id': booking.id,
                'client_name': booking.client_name,
                'dates': booking.dates,
                'gallery_images': booking.gallery_images or [],
                'session_type': booking.session_type,
                'status': booking.status,
                'created_at': booking.created_at.strftime('%Y-%m-%d'),
                'duration': booking.duration,
                'location': booking.location,
                'testimonial': getattr(booking, 'testimonial', '')
            }
            bookings.append(booking_data)
        
        return JsonResponse(bookings, safe=False)
        
    except Exception as e:
        logger.error(f"Failed to fetch bookings: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def upload_gallery_image(request, booking_id):
    """Upload gallery image for a booking"""
    try:
        logger.info(f"Upload request received for booking {booking_id}")
        booking = get_object_or_404(BookingSession, pk=booking_id)

        if request.method == 'POST':
            file = None
            for key in request.FILES:
                file = request.FILES[key]
                break

            if file:
                # Save file to media/gallery/<booking_id>/
                gallery_dir = os.path.join(settings.MEDIA_ROOT, 'gallery', str(booking_id))
                os.makedirs(gallery_dir, exist_ok=True)
                file_path = os.path.join(gallery_dir, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_url = f'/media/gallery/{booking_id}/{file.name}'

                # Update booking.gallery_images
                images = booking.gallery_images or []
                images.append(file_url)
                booking.gallery_images = images
                booking.save()

                return JsonResponse({'url': file_url, 'status': 'success'}, status=200)

            return JsonResponse({'error': 'No file found'}, status=400)

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_booking_gallery(request, booking_id):
    """Get gallery images for a booking"""
    try:
        booking = get_object_or_404(BookingSession, pk=booking_id)
        return JsonResponse({
            'gallery_images': booking.gallery_images or [],
            'testimonial': booking.testimonial or ''
        })
    except Exception as e:
        logger.error(f"Gallery fetch failed: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

