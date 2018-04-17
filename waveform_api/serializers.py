from rest_framework import serializers
from waveform_api.models import Conversation, Comment

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','text', 'time_of_conversation')
    
    def create(self, validated_data):
        conversation_id = self.context['conversation_id']
        conversation = Conversation.objects.get(id=conversation_id)
        comment = Comment.objects.create(
            conversation=conversation,
            **validated_data)
        return comment

class ConversationSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ('id', 'user', 'customer', 'longest_user_monologue', 'longest_customer_monologue', 
                'user_talk_percentage', 'comments')