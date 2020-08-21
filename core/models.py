from django.db import models

# Create your models here.


class Column(models.Model):

    id = models.IntegerField(primary_key=True)
    challenger = models.ForeignKey('core.Challenger', on_delete=models.SET_NULL, blank=True, null=True, related_name="column")
    exercise = models.ForeignKey('core.Exercise', on_delete=models.SET_NULL, blank=True, null=True)

    def __repr__(self):
        return "column {0} - {1} - {2}".format(str(self.id), self.challenger, self.exercise)

    def __str__(self):
        return "column {0} - {1} - {2}".format(str(self.id), self.challenger, self.exercise)

    class Meta:
        db_table = "column"
        verbose_name_plural = "columns"

class Challenger(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    exercises = models.ManyToManyField('core.Exercise', related_name='challenger')
    timezone = models.CharField(max_length=70, blank=True, null=True)


    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = "challenger"
        verbose_name_plural = "challengers"


class Exercise(models.Model):
    EXERCISE_PLANKS = 'planks'
    EXERCISE_BURPEES = 'burpees'
    EXERCISE_CRUNCHES = 'crunches'
    EXERCISE_STEPS = 'steps'
    EXERCISE_MILES = 'miles'
    EXERCISE_PULLUPS = 'pullups'
    EXERCISE_SQUATS = 'squats'
    EXERCISE_PUSHUPS = 'pushups'
    EXERCISE_SUNSALUTES = 'sunsalutes'

    EXERCISE_CHOICES = (
        (EXERCISE_PLANKS, 'Planks'),
        (EXERCISE_BURPEES, 'Burpees'),
        (EXERCISE_CRUNCHES, 'Crunches'),
        (EXERCISE_STEPS, 'Steps'),
        (EXERCISE_MILES, 'Miles'),
        (EXERCISE_PULLUPS, 'Pullups'),
        (EXERCISE_SQUATS, 'Squats'),
        (EXERCISE_PUSHUPS, 'Pushups'),
        (EXERCISE_SUNSALUTES, 'Sun Salutes'),
    )


    name = models.CharField(max_length=200, choices=EXERCISE_CHOICES, default=EXERCISE_PLANKS)
    sms_code = models.CharField(max_length=5)

    def __repr__(self):
        return "{0} ({1})".format(self.name, self.sms_code)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.sms_code)
    
    class Meta:
        db_table = "exercise"
        verbose_name_plural = "exercises"

