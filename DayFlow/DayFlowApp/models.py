from django.contrib.auth.models import User
from django.db import models

WEEKDAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]

WEEKDAYS_SHORT = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}


class Task(models.Model):
    """A user's task: one-time (on a specific date) or
    recurring on chosen weekdays (like an alarm)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description', blank=True)
    time = models.TimeField('Time')

    is_recurring = models.BooleanField('Recurring task', default=False)
    repeat_days = models.CharField(
        'Repeat days',
        max_length=20,
        blank=True,
        help_text='Weekday numbers separated by commas (0=Mon ... 6=Sun)',
    )
    date = models.DateField('Date', null=True, blank=True)

    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

    def get_repeat_days_list(self):
        if not self.repeat_days:
            return []
        return [int(d) for d in self.repeat_days.split(',') if d != '']

    def repeat_days_display(self):
        days = self.get_repeat_days_list()
        return ' · '.join(WEEKDAYS_SHORT[d] for d in sorted(days))

    def occurs_on(self, some_date):
        """Checks whether the task should appear on a given day."""
        if self.is_recurring:
            return some_date.weekday() in self.get_repeat_days_list()
        return self.date == some_date


class TaskCompletion(models.Model):
    """A completion mark for a task on a specific day. Kept separate
    from Task so a recurring task can be completed on each day independently."""

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('task', 'date')