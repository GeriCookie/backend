from django.shortcuts import render
from waveform_api.models import Conversation, Comment
from rest_framework import generics
from waveform_api.serializers import ConversationSerializer, CommentsSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ConversationList(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class ConversationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    lookup_url_kwarg = 'conversation_id'

    def get_queryset(self):
        conversation_id = self.kwargs.get(self.lookup_url_kwarg)
        comments = Conversation.objects.get(id=conversation_id).comments.all()
        return comments

    def get_serializer_context(self):
        return {"conversation_id": self.kwargs.get(self.lookup_url_kwarg)}

class CommentsDetail(APIView):
    serializer_class = CommentsSerializer

    def get_object(self, conversation_id, pk):
        try:
            return Conversation.objects.get(id=conversation_id).comments.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, conversation_id, pk, format=None):
        comment = self.get_object(conversation_id, pk)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)

    def put(self, request, conversation_id, pk, format=None):
        comment = self.get_object(conversation_id, pk)
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, conversation_id, pk, format=None):
        comment = self.get_object(conversation_id, pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)