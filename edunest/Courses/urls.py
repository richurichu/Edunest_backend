from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')


router.register(r'courses-adv', Course_advertis, basename='course_adv')

router.register(r'courses-requests', Course_requests, basename='course_request')

urlpatterns = [
     path('', include(router.urls)),
     path('apply/', CreateApplicationView.as_view(), name='apply-course'),
     path('img-upload/', CourseImageView.as_view(), name='course-image-upload'),
     path('approve_application/<int:application_id>/', ApplicationApproval.as_view(), name='approve_application'),
     path('create-chapter/', ChapterCreateView.as_view(), name='create-chapter'),
     path('chapters/', ChapterListView.as_view(), name='chapter-list'),
     path('toggleLike/<int:chapter_id>/', ChapterLikeToggle.as_view(), name='toggleLike'),

     path('purchased-courses/<int:user_id>/', PurchasedCoursesView.as_view(), name='purchased-course'),


     
     path('courses/<int:course_id>/chapters/', ChaptersByCourse.as_view(), name='chapters-by-course'),
     path('handle_payment/', HandlePaymentView.as_view(), name='handle_payment'),

     path('applications/<int:application_id>/chapters/', ChaptersForCourses.as_view(), name='application-chapters'),
     path('chapter/<int:id>/', ChapterEditDeleteView.as_view(), name='chapter-update'),
     path('approved-applications/', ApprovedApplicationsListView.as_view(), name='approved-applications'),
]