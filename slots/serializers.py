from rest_framework import serializers
from .models import Slot


class SlotSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slot
        fields = '__all__'
        
    def validate(self, attrs):
        user_id = attrs.get('user_id')
        date = attrs.get('date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        user_role = attrs.get('role')

        if user_role not in ['candidate', 'interviewer']:
            raise serializers.ValidationError({'role': 'Role should be either candidate or interviewer'})
                
        if start_time >= end_time:
            raise serializers.ValidationError('Start date should be less than end date')
        
        if Slot.objects.filter(user_id=user_id, date=date,
                               start_time__lt=end_time, end_time__gt=start_time,
                               role=user_role).exists():
            raise serializers.ValidationError('Slot already exists for this user in the given time range')
        
        return attrs