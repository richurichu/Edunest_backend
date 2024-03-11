from django.urls import path
from .views import *

urlpatterns = [
    path('get-families-and-check-payment/<int:user_id>/', GetFamiliesAndCheckPayment.as_view(), name='get_families_and_check_payment'),
    path('create-family/', FamilyCreateView.as_view(), name='family_create'),
    path('get-family/<int:user_id>/', FamilyListView.as_view(), name='family-view'),
    path('get-messages/<int:room_id>/', GetMessages.as_view(), name='get_families_and_check_payment'),
    path('get-members/<int:room_id>/', MembersListView.as_view(), name='get_families_members'),
    path('join-family/<int:user_id>/<int:fam_Id>/', JoinFamilyMember.as_view(), name='join_members'),
    path('block-members/<int:Id>/', BanFamilyMember.as_view(), name='block_members'),
    path('leave-family/<int:user_id>/<int:room_id>/', LeaveFamily.as_view(), name='leave_family'),
    path('Owner-leave-family/<int:user_id>/<int:toBeOwnerId>/<int:room_id>/', AdminLeaveFamily.as_view(), name='admin_leave_family'),
    path('delete-family/<int:room_id>/', DeleteFamily.as_view(), name='delete_family'),

    path('create-messages/', Chatmessages.as_view(), name='chat-messages'),
]