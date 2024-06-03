from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import AccuknoxUsers, FriendRequest
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from . models import AccuknoxUsers
from . serializers import SearchUserSerializer,CustomTokenObtainPairSerializer,UserSignupSerializer, FriendRequestSerializer


# class UserSignupView(generics.ListCreateAPIView):
class UserSignupView(generics.CreateAPIView):
    queryset = AccuknoxUsers.objects.all()
    serializer_class = UserSignupSerializer

class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    serializer_class = SearchUserSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AccuknoxUsers.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            search = search.lower()
            queryset = queryset.filter(
                Q(email__iexact=search) |
                Q(first_name__icontains=search)
            )
        return queryset


class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        to_user = serializer.validated_data['to_user']
        from_user = self.request.user

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError('Friend request already sent.')

        recent_requests = FriendRequest.objects.filter(
            from_user=from_user,
            timestamp__gte=timezone.now() - timedelta(minutes=1)
        ).count()

        if recent_requests >= 3:
            raise serializers.ValidationError('Cannot send more than 3 friend requests within a minute.')

        serializer.save(from_user=from_user)

class AcceptFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.is_accepted = True
        friend_request.save()
        return Response({'status': 'Friend request accepted.'}, status=status.HTTP_200_OK)

class RejectFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.is_rejected = True
        friend_request.save()
        return Response({'status': 'Friend request rejected.'}, status=status.HTTP_200_OK)

class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    pagination_class = UserPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            (Q(from_user=self.request.user) & Q(is_accepted=True)) |
            (Q(to_user=self.request.user) & Q(is_accepted=True))
        )

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    pagination_class = UserPagination
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, is_accepted=False, is_rejected=False)

