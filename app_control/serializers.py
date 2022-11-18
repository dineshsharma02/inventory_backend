from .models import Inventory,InventoryGroup
from rest_framework import serializers

from user_control.serializers import CustomUserSerializer


class InventoryGroupSerialzer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only = True)
    created_by_id = serializers.CharFieldZ(write_only = True, required = False)
    belongs_to = serializers.SerializerMethodField(read_only = True)
    belong_to_id = serializers.CharField(write_only = True)
    total_items = serializers.CharField(read_only = True, required = False)

    class Meta:
        model = InventoryGroup
        fields = "__all__"

    def get_belongs_to(self,obj):
        if obj.belongs_to is not None:
            return InventoryGroupSerialzer(obj.belongs_to).data
        return None

class InventorySerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only = True)
    created_by_id = serializers.CharField(write_only = True, required = False)
    group = InventoryGroupSerialzer(read_only = True)
    group_id = serializers.CharField(write_only = True)

    class Meta:
        model = Inventory
        fields = "__all__"

        