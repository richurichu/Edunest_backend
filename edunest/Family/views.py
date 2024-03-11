from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Families
from Courses.models import Payment
from .serializers import *
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404



class GetFamiliesAndCheckPayment(APIView):
    def get(self, request, user_id):
        families = Families.objects.all().order_by('-created_on')
        user = CustomUser.objects.get(pk=user_id)
        serializer = FamilySerializer(families, many=True)
        
        is_user_paid = Payment.objects.filter(user_id=user_id).exists()
        has_family = user.family is not None
        is_owner = Families.objects.filter(owner = user ).exists()
        if is_owner:
            is_owner = True
        else:
            is_owner=False
        response_data = {
            'families': serializer.data,
            'is_user_paid': is_user_paid,
            'has_family':has_family,
            'is_owner':is_owner
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class FamilyCreateView(ListCreateAPIView):
    
    queryset = Families.objects.all()
    
    serializer_class = FamilyCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
       
        name = self.request.data.get('name')
        instruction = self.request.data.get('instruction')
        user_id = self.request.data.get('user')
        image = self.request.data.get('image')
        user = CustomUser.objects.get(pk=user_id)
        existing_family = Families.objects.filter(owner=user).first()

        if existing_family:
           
             raise serializers.ValidationError("You already have a family. You cannot create a new one.")
        else:
            if 'image' in self.request.data:
                image = self.request.data.get('image')
                serializer.save( instruction=instruction, name=name, family_image=image ,owner=user)
            else:
                serializer.save(owner=user, name=name ,instruction=instruction)

class FamilyListView(APIView):

    def get(self , request ,user_id):
       

        user = CustomUser.objects.get(pk=user_id)
        if user.family :
          
            fam_name = user.family.name
            fam_id = user.family.pk
            owner_id = user.pk
          
            members_count = CustomUser.objects.filter(family = user.family).count()

            return Response({'fam_name':fam_name , 'fam_id': fam_id ,'members_count':members_count, 'owner_id': owner_id})
        else:
            fam = Families.objects.get(owner = user)
            members_count = CustomUser.objects.filter(family = fam).count()
            fam_name = fam.name
            fam_id = fam.pk
            owner_id = user.pk
            return Response({'fam_name':fam_name , 'fam_id': fam_id ,'members_count':members_count , 'owner_id':owner_id})
        

            
class MembersListView(APIView):
    
    def get(self , request ,room_id):
       
        fam = Families.objects.get(pk = room_id)
        members = CustomUser.objects.filter(family = fam)
        serializers = CustomUserSerializer( members,many =True)
        return Response(serializers.data)

class BanFamilyMember(APIView):

    def post(self , request ,Id):
       
        user = CustomUser.objects.get(id = Id)
        user.family = None
        user.save()
        return Response('succesfully banned')
    
class JoinFamilyMember(APIView):

    def post(self , request ,user_id ,fam_Id):
       
        user = CustomUser.objects.get(id = user_id)
        family = Families.objects.get(id= fam_Id)
        user.family = family
        user.save()
        return Response('Joined succesfully')
    
class DeleteFamily(APIView):

    def post(self , request , room_id):
       
        family = Families.objects.get(id = room_id)
        family.delete()
        return Response('Family deleted succesfully')
    

class LeaveFamily(APIView):

    def post(self , request , user_id, room_id):
       
        user = CustomUser.objects.get(id = user_id)
        if user.family:
            user.family = None
            user.save()
            return Response('Leaved succesfully')
        
        family = Families.objects.get(id= room_id)
        family.owner = None
        family.save()
        return Response('Leaved succesfully')
    
class AdminLeaveFamily(APIView):

    def post(self , request , user_id, toBeOwnerId, room_id):
       
        user = CustomUser.objects.get(id = user_id)
        TobeOwner = CustomUser.objects.get(id = toBeOwnerId)


        # if user.family:
        #     user.family = None
        #     user.save()
        
        family = Families.objects.get(id= room_id)
        TobeOwner.family = None
        family.owner = TobeOwner
        user.family = None
       
        TobeOwner.save()
        family.save()
        user.save()
        return Response('Owner removed  succesfully and New admin is appointed ')
        
class GetMessages(APIView):
    def get(self, request, room_id):
        messages = Message.objects.filter(family=room_id)
        serializer = MessagesSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Chatmessages(APIView):
    
    
    def post(self,request,):
       
        text = request.data['text']
        sender = request.data['sender']
        family_id = request.data['room_id']

        if family_id:
            family = Families.objects.get(pk=family_id)
            Message.objects.create(
                family=family,
                sender=sender,
                text=text
            )

        return Response({'message': 'mesg  created successfully '})