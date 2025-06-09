from rest_framework.routers import DefaultRouter
from .api import FitnessClassViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'classes', FitnessClassViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = router.urls