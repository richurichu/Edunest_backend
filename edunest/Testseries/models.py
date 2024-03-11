from django.db import models


class TestSeries(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    faculty = models.ForeignKey('authentification.CustomUser',on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    def has_user_attended(self, user):
        
        return TestAttempt.objects.filter(user=user, testseries=self).exists()

    def __str__(self):
        return self.name

    def __str__(self):
        
        return self.name


class Question(models.Model):
    test_series = models.ForeignKey(TestSeries, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE )
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text
    
class TestAttempt(models.Model):
    user  = models.ForeignKey('authentification.CustomUser',on_delete=models.CASCADE)
    testseries = models.ForeignKey(TestSeries,on_delete=models.CASCADE)
    created_on = models.DateTimeField()


class QuizResponse(models.Model):
    testattempt = models.ForeignKey(TestAttempt,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE , null = True, blank=True, related_name='selected_opt')
    correct_option = models.ForeignKey(Option, on_delete=models.CASCADE ,related_name='correct_opt')
    is_bookmarked = models.BooleanField(default=False)


