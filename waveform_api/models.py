from django.db import models
from django.contrib.postgres.fields import ArrayField
import os

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
                    models.FloatField(null=True, blank=True, default=None),
                    size=2,
                ),
    )

    customer = ArrayField(
                    ArrayField(
                        models.FloatField(null=True, blank=True,
                                          default=None),
                        size=2
                    )
    )
    def _create_conversation(self):
        self.user = self._parse_log('user')
        self.customer = self._parse_log('customer')
        self.longest_user_monologue = self._monologue_calc(
            self.user
        )
        self.longest_customer_monologue = self._monologue_calc(
            self.customer
        )
        self.user_talk_percentage = self._calc_talk_percentage(
            self.user
        )
        return self
    
    def _calc_talk_percentage(self, arr):
        durations_arr = list(map(self._duration, arr))
        talk_percentage = sum(durations_arr)/arr[-1][1]

    def _duration(self, durations_arr):
        return durations_arr[1] - durations_arr[0]

    def _monologue_calc(self, arr):
       durations_arr = list(map(self._duration, arr))
       return max(durations_arr)

    def _parse_log(self, log_type):
        # needed for opening the log file
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        if log_type == 'user':
            log_file = open(os.path.join(__location__,'user-channel.txt'), 'r')
        elif log_type == 'customer':
            log_file = open(os.path.join(__location__,'customer-channel.txt'), 'r')

        results = []
        index_of_seconds = 4
        first_value = 0
        last_value = 1863.166625
        while True:
            from_to_arr = []
            if len(results) == 0:
                first_line = log_file.readline()
                first_line = first_line.split()
                from_to_arr.append(first_value)
                from_to_arr.append(float(first_line[index_of_seconds]))
                results.append(from_to_arr)
                from_to_arr = []
            silence_end_line = log_file.readline()
            silence_start_line = log_file.readline()
            if not silence_end_line and not silence_start_line:
                # magic end value for integrity in the array 
                results[-1].append(last_value)
                break
            silence_end_line = silence_end_line.split()
            silence_start_line = silence_start_line.split()
            if 'silence_end:' in silence_end_line:
                from_to_arr.append(float(silence_end_line[index_of_seconds]))
            if 'silence_start:' in silence_start_line:
                from_to_arr.append(float(silence_start_line[index_of_seconds]))
            results.append(from_to_arr)
            from_to_arr = []
        return results

    def save(self, *args, **kwargs):
        if not self.pk:
            import ipdb; ipdb.set_trace()
            self._create_conversation()
        super(Conversation, self).save(args, kwargs)

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text =  models.CharField(max_length=100000, default=None)
    time_of_conversation = models.CharField(max_length=100, default=None)
    conversation = models.ForeignKey(Conversation, default=None,
                                     on_delete=models.CASCADE,
                                     related_name='comments')
