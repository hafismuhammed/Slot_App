from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Slot
from .serializers import SlotSerializer
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateSlotAPIView(APIView):
    """API for candidates/interviewers to register their available time slots
    """
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id", "role", "date", "start_time", "end_time"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    example=1, 
                    description="ID of the user ('Interviewer or Candidate)"
                ),
                "role": openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    example="candidate", 
                    description="Role of the user (either 'candidate' or 'interviewer')"
                ),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    format="date", 
                    example="2025-02-20", 
                    description="Date for which the availability is being set (YYYY-MM-DD)"
                ),
                "start_time": openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    format="time", 
                    example="15:00:00", 
                    description="Start time of availability (24-hour format HH:MM:SS)"
                ),
                "end_time": openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    format="time", 
                    example="20:00:00", 
                    description="End time of availability (24-hour format HH:MM:SS)"
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Slot added successfully!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Slot added successfully!")
                    }
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, example="Invalid input data")
                    }
                ),
            ),
        },
    )
    def post(self, request):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Slot added successfully!"}, 
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SlotAvailabilityAPIView(APIView):
    """API which will return interview schedulable time slots as a list
    """
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Date for which slots are needed (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                "interviewer_id",
                openapi.IN_QUERY,
                description="User ID of the interviewer",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                "candidate_id",
                openapi.IN_QUERY,
                description="User ID of the candidate",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                "Available interview slots",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Available slots"),
                        "slots": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                example=[
                                    ["10:00:00", "11:00:00"],
                                    ["11:00:00", "12:00:00"],
                                    ]
                            )
                        )
                    }
                )
            ),
            404: openapi.Response(
                "No slots available",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="No slots available"),
                        "slots": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                            example=[]
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        date = request.GET.get('date')
        interviewer_id = request.GET.get('interviewer_id')
        candidate_id = request.GET.get('candidate_id')

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
        

