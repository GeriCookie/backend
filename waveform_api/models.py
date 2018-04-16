from django.db import models
from django.contrib.postgres.fields import ArrayField


class Conversation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    longest_user_monologue = models.FloatField(null=True, blank=True,
                                               default=None)
    longest_customer_monologue = models.FloatField(null=True, blank=True,
                                                   default=None)
    user_talk_percentage = models.FloatField(null=True, blank=True,
                                             default=None)
    user = ArrayField(
                ArrayField(
                    models.FloatField(null=True, blank=True, default=None)
                )
    )

    customer = ArrayField(
                    ArrayField(
                        models.FloatField(null=True, blank=True, default=None)
                    )
    )


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text =  models.CharField(max_length=100000, default=None)
    time_of_conversation = models.CharField(max_length=100, default=None)
    conversation = models.ForeignKey(Conversation, default=None,
                                     on_delete=models.CASCADE,
                                     related_name='comments')
