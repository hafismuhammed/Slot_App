from django.urls import path
from .views import CreateSlotAPIView, SlotAvailabilityAPIView


urlpatterns = [
    path('create-slot/', CreateSlotAPIView.as_view(), name='create slot API'),
    path('slot-availability/', SlotAvailabilityAPIView.as_view(), name='slot availability API'),
]

