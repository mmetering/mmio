from django.db import models


class NotificationPin(models.Model):
    name = models.CharField(max_length=30)
    pin = models.IntegerField()

    def __str__(self):
        return 'Pin %d: %s' % (self.pin, self.name)

    class Meta:
        verbose_name = 'Benachrichtigungspin'
        verbose_name_plural = 'Benachrichtigungspins'
