from django.shortcuts import render
from rest_framework import viewsets,status
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
 




class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        chapter_id = self.request.query_params.get('chapter_id')
        if chapter_id:
            return Comment.objects.filter(video_chapter=chapter_id)
        else:
           
            return Comment.objects.none()
    
    # def post(self, request, chapter_id,user):
      
    #     data = request.data
        
    #     data['user'] = user  
    #     data['video_chapter'] = chapter_id

    #     serializer = CommentSerializer(data=data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chapter_id):
        text = request.data.get('text')
        chapter = Chapter.objects.get(pk=chapter_id)
        user = request.user  # This is the authenticated user
        if request.data.get('parentid'):
             
             id = request.data.get('parentid')
            
             parent = Comment.objects.get(pk=id)

             comment = Comment.objects.create(
             user=user,
             video_chapter=chapter,
             text=text,
             parent_comment = parent
        )

             serializer = CommentCreateSerializer(comment)

             return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Create a new comment with the provided data
        comment = Comment.objects.create(
            user=user,
            video_chapter=chapter,
            text=text
        )

        serializer = CommentCreateSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ReplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chapter_id):
        text = request.data.get('text')
        id = request.data.get('parentid')
        chapter = Chapter.objects.get(pk=chapter_id)
        user = request.user  # This is the authenticated user
        
       
        parent = Comment.objects.get(pk=id)

        comment = Comment.objects.create(
        user=user,
        video_chapter=chapter,
        text=text,
        parent_comment = parent)
        

        serializer = ReplyCreateSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentEditDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = EditDeleteSerializer
    lookup_field = 'id'

class QuestionListCreateView(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Discussion.objects.all().order_by('-created_at')
    
    serializer_class = QuestionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        content = self.request.data.get('content')
        user_id = self.request.data.get('user')
        image = self.request.data.get('image')
        user = CustomUser.objects.get(pk=user_id)
        
        if 'image' in self.request.data:
            image = self.request.data.get('image')
            serializer.save(user=user, content=content, image=image)
        else:
            serializer.save(user=user, content=content)


class QuestionUpdateView(UpdateAPIView):
   
    queryset = Discussion.objects.all()
    serializer_class = QuestionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        content = self.request.data.get('content')
        image = self.request.data.get('image')

        if 'image' in self.request.data:
            
            serializer.save(content=content, image=image)
        else:
            
            serializer.save(content=content)


class QuestionDeleteView(DestroyAPIView):
    queryset = Discussion.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


# class DiscussionRepliesViewSet(viewsets.ModelViewSet):
#     queryset = Discussion_Comment.objects.all()
#     serializer_class = DiscussionCommentSerializer


class DiscussionRepliesViewSet(viewsets.ModelViewSet):
    
    queryset = Discussion_Comment.objects.all()
    serializer_class = DiscussionCommentSerializer

    def get_queryset(self):
        Question_id = self.request.query_params.get('Question_id')
        if Question_id:
            return Discussion_Comment.objects.filter(question=Question_id).order_by('-created_at')
        else:
           
            return Discussion_Comment.objects.none()       


class DiscussionResponseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, Question_id):
        user = request.user
        text = request.data.get('text', '')
        audio = request.data.get('audio')

        try:
            question = Discussion.objects.get(pk=Question_id)
        except Discussion.DoesNotExist:
            return Response("Question not found", status=status.HTTP_404_NOT_FOUND)

        comment = Discussion_Comment(
            question=question,
            user=user,
           
        )

        if audio:
            comment.audio = audio
        if text:
            comment.text = text

        comment.save()
        serializer = DiscussionResponseCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    
class DiscussionEditDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Discussion_Comment.objects.all()
    serializer_class = DiscussionCommentEditDeleteSerializer
    lookup_field = 'id'



class DiscussionNestedReplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, Question_id):
        user = request.user
        text = request.data.get('text', '')
        audio = request.data.get('audio')
        id = request.data.get('parentid')

        parent =Discussion_Comment.objects.get(pk=id)

        try:
            question = Discussion.objects.get(pk=Question_id)
        except Discussion.DoesNotExist:
            return Response("Question not found", status=status.HTTP_404_NOT_FOUND)

        comment = Discussion_Comment(
            question=question,
            user=user,
            parent_comment=parent,
           
        )

        if audio:
            comment.audio = audio
        if text:
            comment.text = text

        comment.save()
        serializer = DiscussionNestedCommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    