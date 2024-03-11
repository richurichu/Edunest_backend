from django.urls import path
from .views import *

urlpatterns = [


    path('create-quiz/', CreateQuiz.as_view(), name='create-quizlist '),
    path('get-quizlist/', QuizListView.as_view(), name='quizlist '),

    path('get-quiz_admin/', AdminQuizView.as_view(), name='testseries_admin'),


    path('get-quiz_faculty/', FacultyQuizView.as_view(), name='testseries_faculty'),
    path('publish-quiz_faculty/', FacultyQuizPublish.as_view(), name='publish_testseries_faculty'),
    path('unpublish-quiz_faculty/', FacultyUnQuizPublish.as_view(), name='unpublish_testseries_faculty'),

    path('create-questions-quiz_faculty/', FacultyQuizCreate.as_view(), name='testseries_create_faculty'),
    path('update-questions-quiz_faculty/', FacultyQuizUpdate.as_view(), name='testseries_update_faculty'),

    path('get-quiz/<int:testseries_id>/', TestseriesDetailAPI.as_view(), name='testseries'),
    path('get-quiz_faculty/<int:testseries_id>/', FacultyTestseriesDetailAPI.as_view(), name='testseries_faculty'),

    path('get-marks/', CalculateMarksAPIView.as_view(), name='testseries-marks'),
    
    path('get-answerkey/<int:user_id>/<int:testseries_id>/', QuizResponseListView.as_view(), name='testseries-answerkey'),
    path('toggle_bookmark/<int:quiz_response_id>/', Handlebookmark.as_view(), name='toggle_bookmark'),
    path('saved-questions/<int:user_id>/', UserBookmarkedResponses.as_view(), name='saved_questions'),
    path('top-users/', TopUsersListView.as_view(), name='top-users-list'),
    
]