from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from waveform_api import views

urlpatterns = [
    url(r'^conversations/$', views.ConversationList.as_view()),
    url(r'^conversations/(?P<pk>[0-9]+)/$', views.ConversationDetail.as_view()),
    url(r'^conversations/(?P<conversation_id>[0-9]+)/comments/$', views.CommentsList.as_view()),
    url(r'^conversations/(?P<conversation_id>[0-9]+)/comments/(?P<pk>[0-9]+)/$', views.CommentsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)