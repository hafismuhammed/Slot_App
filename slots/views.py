from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Slot
from .serializers import SlotSerializer
from datetime import datetime, timedelta


class CreateSlotAPIView(APIView):
    
    def post(self, request):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Availability registered successfully!"}, 
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SlotAvailabilityAPIView(APIView):
    
    def post(self, request):
        date = request.data.get('date')
        interviewer_id = request.data.get('interviewer_id')
        candidate_id = request.data.get('candidate_id')

        interviewer_slots = Slot.objects.filter(role='interviewer', user_id=interviewer_id, date=date)
        candidate_slots = Slot.objects.filter(role='candidate', user_id=candidate_id, date=date)
        
        if not interviewer_slots.exists() or not candidate_slots.exists():
            return Response(
                {"message": "No slots available", "slots": []},
                status=status.HTTP_404_NOT_FOUND
                )
            
        available_slots = []
        for candidate_slot in candidate_slots:
            
            for interviewer_slot in interviewer_slots:
                start_time = max(candidate_slot.start_time, interviewer_slot.start_time)
                end_time = min(candidate_slot.end_time, interviewer_slot.end_time)
                
                start_time_obj = datetime.strptime(str(start_time), '%H:%M:%S')
                end_time_obj = datetime.strptime(str(end_time), '%H:%M:%S')
                
                while start_time_obj + timedelta(hours=1) <= end_time_obj:
                    slot_start_time = start_time_obj.strftime('%H:%M:%S')
                    slot_end_time = (start_time_obj + timedelta(hours=1)).strftime('%H:%M:%S')
                    available_slots.append(
                           (slot_start_time, slot_end_time)
                           )
                    
                    start_time_obj += timedelta(hours=1)
        return Response(
            {"message": "Available slots", "slots": available_slots},
            status=status.HTTP_200_OK
            )
        

