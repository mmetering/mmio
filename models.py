from django.db import models


class NotificationPin(models.Model):
    STATE_TYPES = (
        ('E', 'Error'),
        ('W', 'Working'),
    )
    name = models.CharField(max_length=30)
    pin = models.IntegerField(unique=True)
    state = models.CharField(max_length=2, choices=STATE_TYPES, default='W')

    def __str__(self):
        return 'Pin %d: %s' % (self.pin, self.name)

    class Meta:
        verbose_name = 'Benachrichtigungspin'
        verbose_name_plural = 'Benachrichtigungspins'
