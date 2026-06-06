from rest_framework import serializers

from .models import Announcement, Broadcast


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"


class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        fields = "__all__"
        read_only_fields = ["status", "total_count", "sent_count", "failed_count", "completed_at"]
