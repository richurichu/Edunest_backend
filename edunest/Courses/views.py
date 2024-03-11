
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Course
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView,DestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser

from  .PaymentSdk import paypalrestsdk

paypalrestsdk.configure({
    "mode": 'sandbox',
    "client_id": 'AbCASLvwWw6V1PZsqomXD4svWf3mQNYlnn8R_CLlfOy8XjqLef6q4btUj99KkXRnv7bh3bHiVH4Shblj',
    "client_secret": 'EFDvGBADnswB9Fl0gd6LuSAA9sOLKcBzo-RRbCCvTS2lQKqIGm--aFpaltdcsyJzFBiMN6vLYvHmgmje'
     })


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-updated_at')
    serializer_class = CourseSerializer

class PurchasedCoursesView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        purchased_courses = user.payment_set.values('course').distinct()
        courses = Course.objects.filter(id__in=purchased_courses)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    
class Course_advertis(viewsets.ModelViewSet):
    queryset = Course_advertise.objects.filter(is_vacant=True).order_by('-updated_at')
    serializer_class = CourseadvSerializer

class Course_requests(viewsets.ModelViewSet):
    queryset = applications.objects.all()
    serializer_class = CourseRequestSerializer

class ApprovedApplicationsListView(ListAPIView):
    queryset = applications.objects.filter(approved=True)
    serializer_class = ApplicationApprovedSerializer


class CourseImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            course = Course.objects.get(teacher=request.user)
        except Course.DoesNotExist:
            return Response({"error": "No course associated with this teacher."}, status=status.HTTP_404_NOT_FOUND)

        image = request.FILES.get('image')

        if not image:
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

        course.image = image
        course.save()

        return Response({"message": "Image uploaded successfully."}, status=status.HTTP_200_OK)

class CreateApplicationView(CreateAPIView):
    queryset = applications.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
       
        course_id = serializer.validated_data.get('course_id')
        course_instance = Course_advertise.objects.get(id=course_id)

        has_applied = applications.objects.filter(user_id=user, course_id=course_instance).exists()

        if has_applied:
            raise serializers.ValidationError("You have already applied for this Vacancy!")

        serializer.save(user_id=user,course_id=course_instance)

class ApplicationApproval(APIView):

    def post(self, request, application_id):
        application = get_object_or_404(applications, id=application_id)
       
        
        # Check if the user is already a teacher by checking their mainrole
        if application.user_id.role == 'TEACHER':
            return Response({"message": "This user is already a teacher for another course."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the course is already filled
        if not application.course_id.is_vacant:
            return Response({"message": "This course already has a teacher."}, status=status.HTTP_400_BAD_REQUEST)
        

        new_course = Course(
            name=application.course_id.name,
            price=application.course_id.price,
            teacher=application.user_id
            
        )
        new_course.save()
        application.approved = True
        application.save()
       
        application.course_id.is_vacant = False
        application.course_id.save()

        application.user_id.role = 'TEACHER'
        application.user_id.save()

        return Response({"message": "Application approved and user is now the course teacher."})

class ChapterListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ChapterViewSerializer

    def get_queryset(self):
       
        try:
            course = Course.objects.get(teacher=self.request.user)
           
            return Chapter.objects.filter(course=course)
        except Course.DoesNotExist:
            return Chapter.objects.none()



class ChapterCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def perform_create(self, serializer):
        try:
            course = Course.objects.get(teacher=self.request.user)
            if not course.image:
                raise ValidationError("Adding cover image is compulsory")
        except Course.DoesNotExist:
            raise ValidationError({"error": "No course associated with this teacher."})
        
        current_chapters_count = Chapter.objects.filter(course=course).count()

        is_free_chapter = current_chapters_count in [0, 1]


        serializer.save(course=course , is_free = is_free_chapter)


class ChapterLikeToggle(APIView):
   
    permission_classes = [IsAuthenticated]

    def post(self, request,chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        user = request.user 

        try :
            chapter_liked = ChapterLiked.objects.get(user=user,chapter=chapter)
        except ChapterLiked.DoesNotExist:
               ChapterLiked.objects.create(user= user , chapter = chapter,is_liked = True)
               chapter.Likes_count += 1
               chapter.save()
               return Response({'success': 'Like status updated successfully'}, status=status.HTTP_200_OK)
        
        if chapter_liked.is_liked == False:
            chapter.Likes_count += 1
        else:
             chapter.Likes_count -= 1
        chapter.save()
       
        chapter_liked.is_liked = not chapter_liked.is_liked
        chapter_liked.save()
        likes_count = ChapterLiked.objects.filter(chapter__id=chapter_id, is_liked=True).count()

        response_data = {
            'is_liked': chapter_liked.is_liked,
            'likes_count': likes_count,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

    def get(self, request,chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        user = request.user 

        try :
            chapter_liked = ChapterLiked.objects.get(user=user,chapter=chapter)
        except ChapterLiked.DoesNotExist:
            chapter_liked = ChapterLiked(is_liked=False)
               
        
        likes_count = ChapterLiked.objects.filter(chapter__id=chapter_id, is_liked=True).count()
        if likes_count == 0:
           likes_count = 0


        response_data = {
            'is_liked': chapter_liked.is_liked,
            'likes_count': likes_count,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class ChaptersForCourses(RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        application_id = self.kwargs.get('application_id')
       
        try:
            application_instance = applications.objects.get(id=application_id)
           
            course_advertise_instance = application_instance.course_id
           
            course_instance = Course.objects.get(name=course_advertise_instance.name)
           
            chapters = Chapter.objects.filter(course=course_instance)
            
            # Serialize the chapters
            serializer = ChapterViewSerializer(chapters, many=True)
            return Response(serializer.data)
        except applications.DoesNotExist:
            return Response({"error": "Application not found."}, status=400)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=400)
        
        
class ChapterEditDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Chapter.objects.all()
    serializer_class = ChapterEditSerializer
    lookup_field = 'id'  



class ChaptersByCourse(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):

        chapters = Chapter.objects.filter(course=course_id).order_by('created')
        user_id = self.request.user.id 
        
        user_has_purchased = Payment.objects.filter(course=course_id, user=user_id).exists()

        if not chapters.exists():
            return Response({"detail": "No chapters found for this course."}, status=status.HTTP_404_NOT_FOUND)
        
       

        serializer = ChapterViewSerializer(chapters, many=True)
        return Response({
            'chapters': serializer.data,
            'purchased': user_has_purchased
        })
                         



     
class HandlePaymentView(APIView):

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('orderId')  
       
       
        course_id = request.data.get('courseId')

        if order_id and course_id:
            course = Course.objects.get(id=course_id)
           
            Payment.objects.create(
                    user=self.request.user,
                    course=course,
                    order_id=order_id
                )
            return Response({"success": True, "message": "Payment processed successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "Payment validation failed"}, status=status.HTTP_400_BAD_REQUEST)