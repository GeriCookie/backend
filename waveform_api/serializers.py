from rest_framework import serializers
from waveform_api.models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('id', 'user', 'customer', 'longest_user_monologue', 'longest_customer_monologue', 'user_talk_percentage')
