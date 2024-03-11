from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.utils import timezone
from authentification.models import CustomUser
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from authentification import models
from Courses.models import applications
from django.db.models import Count




class QuizListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TestSeries.objects.filter(is_published = True)
    serializer_class = TestSeriesSerializer


class AdminQuizView(APIView):
   
    def get(self,request,):
        
        application_id = self.request.query_params.get('application_id')
        application = get_object_or_404(applications, pk=application_id)
        user_id = get_object_or_404(CustomUser, pk=application.user_id.id)
        testseries = TestSeries.objects.filter(faculty=user_id,is_published=True).annotate(question_count=Count('question'))
        serializers = FacultyTestSeriesSerializer(testseries, many= True)
        return Response(serializers.data)
    


class FacultyQuizView(APIView):

    def get(self,request,):
       
        faculty_id = self.request.query_params.get('faculty_id')
        faculty = get_object_or_404(CustomUser, pk=faculty_id)
        
        testseries = TestSeries.objects.filter(faculty=faculty).annotate(question_count=Count('question'))
        serializers = FacultyTestSeriesSerializer(testseries, many= True)

        return Response(serializers.data)


class FacultyQuizPublish(APIView):

    def patch(self,request,):
        testseries_id = self.request.query_params.get('currentquizid')
        testseries = get_object_or_404(TestSeries,pk=testseries_id)
        testseries.is_published = True
        testseries.save()
        return Response({'message': 'quiz updated successfully'})

class FacultyUnQuizPublish(APIView):

    def patch(self,request,):
        testseries_id = self.request.query_params.get('currentquizid')
        testseries = get_object_or_404(TestSeries,pk=testseries_id)
        testseries.is_published = False
        testseries.save()
        return Response({'message': 'quiz updated successfully'})
    


class FacultyQuizCreate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,):
       
        quiz_id = request.data['quiz_id']
        question = request.data['question']
        options_data = request.data['options']
        quiz = get_object_or_404(TestSeries, pk=quiz_id)
        question_obj = Question.objects.create(
            test_series=quiz,
            text= question

        )
        quest_count = Question.objects.filter(test_series=quiz).count()
        for option_data in options_data:
            option_text = option_data['text']
            is_correct = option_data['isCorrect']

          
            if is_correct:
                is_correct_option = Option.objects.filter(question=question_obj, is_correct=True).exists()
                if not is_correct_option:
                    option_obj = Option.objects.create(
                        question=question_obj,
                        text=option_text,
                        is_correct=True,
                    )
            else:
                option_obj = Option.objects.create(
                    question=question_obj,
                    text=option_text,
                    is_correct=False,
                )

        return Response({'message': 'Options created successfully','quest_count':quest_count})
    


class FacultyQuizUpdate(APIView):
   
    def put(self, request):
        question_data = request.data
        
        question_id = request.data['question_id']
        question_obj = get_object_or_404(Question, pk=question_id)

       
        if 'question' in question_data:
            question_obj.text = question_data['question']
            question_obj.save()
       
        for option_data in question_data.get('options', []):
           
            option_id = option_data.get('id')
            option_text = option_data['text']
            is_correct = option_data['isCorrect']
        
            option_obj = get_object_or_404(Option, pk=option_id)
            option_obj.text = option_text
            option_obj.is_correct = is_correct
            option_obj.save()
           
        return Response({'message': 'Question and options updated successfully'})

class TestseriesDetailAPI(APIView):
   
    def get(self,request,testseries_id,format=None):
       
            
        # test_series = TestSeries.objects.prefetch_related('question_set__option_set').get(id=testseries_id)
        test_series = TestSeries.objects.get(id=testseries_id)
        
        questions = test_series.question_set.all()
        
        questions_dict = {}
        for question in questions:
            
            options = [{'id': option.id, 'text': option.text} for option in question.option_set.all()]
            questions_dict[question.id] = {
                'id': question.id,
                'text': question.text,
                'options': options
    }
        return Response(questions_dict)
    
class FacultyTestseriesDetailAPI(APIView):
    
    def get(self,request,testseries_id,format=None):
       
            
       
        test_series = TestSeries.objects.get(id=testseries_id)
        
        
        questions = test_series.question_set.all()
        
        questions_dict = {}
        for question in questions:
            
            options = [{'id': option.id, 'text': option.text, 'is_correct':option.is_correct} for option in question.option_set.all()]
            questions_dict[question.id] = {
                'id': question.id,
                'text': question.text,
                'options': options
    }
        return Response(questions_dict)
    

        
class CalculateMarksAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        testseries_id = request.data.get('testseries_id')
        response_data = request.data.get('selectedOptions')
        total_marks = 0
        correct_count = 0
        unattempted_count = 0
        incorrect_count = 0

        user = CustomUser.objects.get(pk= user_id)
        testseries = TestSeries.objects.get(pk = testseries_id)

        existing_attempt = TestAttempt.objects.filter(user_id=user_id, testseries_id=testseries_id).first()

        if existing_attempt:
       
           return HttpResponseBadRequest("A TestAttempt already exists for this user and test series.")

        testseries_attempt = TestAttempt.objects.create(
            user = user,
            testseries = testseries,
            created_on = timezone.now()
        )
        all_questions = Question.objects.filter(test_series=testseries)
        
        for question_id, selected_option_id in response_data.items():
            question = Question.objects.get(pk=question_id)
            selected_option = Option.objects.get(pk=selected_option_id)
            correct_option = Option.objects.get(question=question_id, is_correct = True)

            testAttempt_record  = QuizResponse.objects.create(
                testattempt = testseries_attempt,
                question = question,
                selected_option = selected_option,
                correct_option = correct_option
            )

            if selected_option.is_correct:

                total_marks += 1
                correct_count += 1
            else:
                total_marks -= 0.3
                incorrect_count += 1
            
        unattempted_questions = all_questions.exclude(id__in=response_data.keys())
        for unattempted_question in unattempted_questions:
            
            QuizResponse.objects.create(
                testattempt=testseries_attempt,
                question=unattempted_question,
                selected_option=None,
                correct_option=Option.objects.get(question=unattempted_question, is_correct=True)
            )
            unattempted_count += 1

        rounded_total_marks = round(total_marks, 3)
        user.quiz_points += rounded_total_marks
        if user.family:
            user.family.total_points += rounded_total_marks
            user.family.save()
        user.save()


        return Response({'total_marks': rounded_total_marks , 'correct_count':correct_count , 'unattempted_count':unattempted_count ,'incorrect_count':incorrect_count ,'testseries_id':testseries_id})



class QuizResponseListView(ListAPIView):
    serializer_class = QuizResponseSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        testseries_id = self.kwargs['testseries_id']
    
        test_attempt = get_object_or_404(TestAttempt,  user=user_id, testseries=testseries_id)

        quiz_responses= QuizResponse.objects.filter(testattempt=test_attempt)
        
        return quiz_responses
    
class Handlebookmark(APIView):
    
    def post(self,request,quiz_response_id):
        quiz_response = get_object_or_404(QuizResponse, id=quiz_response_id)
        quiz_response.is_bookmarked = not quiz_response.is_bookmarked
        quiz_response.save()
        return Response({'status': 'success', 'is_bookmarked': quiz_response.is_bookmarked})
    
class CreateQuiz(APIView):
    def post(self,request):
        faculty_id = request.data['faculty']
        name = request.data['name']
        description = request.data['description']
        faculty = get_object_or_404(CustomUser, pk=faculty_id)

        quiz = TestSeries.objects.create(
            name= name,
            faculty = faculty,
            description = description

        )
        serializer = QuizCreateSerializer(quiz)

        return Response(serializer.data)
    

class UserBookmarkedResponses(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        
        bookmarked_responses = QuizResponse.objects.filter(
            testattempt__user=user,
            is_bookmarked=True
        )

        serializer = QuizResponseSerializer(bookmarked_responses, many=True)
        return Response(serializer.data)

class TopUsersListView(ListAPIView):
    queryset = CustomUser.objects.exclude(role='TEACHER').order_by('-quiz_points')[:7]
    serializer_class = CustomUserSerializer

