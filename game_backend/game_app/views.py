from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetScoreboard(APIView):
    def get(self, request):
        users = User.objects.all().order_by('-high_score')
        return Response(users.values('user_id', 'high_score'), status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'username', 'last_game_score'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='User ID'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'last_game_score': openapi.Schema(type=openapi.TYPE_INTEGER, description='Last game score')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'high_score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'last_game_score': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            ),
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'high_score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'last_game_score': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
        }
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        last_game_score = request.data.get('last_game_score')
        user = User.objects.filter(user_id=user_id).first()
        if user:
            if last_game_score > user.high_score:
                user.high_score = last_game_score
            user.last_game_score = last_game_score
            user.save()
            return Response({"user_id": user.user_id, "last_game_score": user.last_game_score,"high_score": user.high_score}, status=status.HTTP_200_OK)
        else:
            user = User.objects.create(user_id=user_id, username=username, last_game_score=last_game_score, high_score=last_game_score)
            return Response({"user_id": user.user_id, "last_game_score": user.last_game_score,"high_score": user.high_score}, status=status.HTTP_201_CREATED)
    

class GetUser(APIView):
    def get(self, request, user_id):
        
        user = User.objects.filter(user_id=user_id).first()

        if user:
            return Response({"user_id": user.user_id, 
                            "username": user.username,
                            "last_game_score": user.last_game_score,
                            "high_score": user.high_score,
                            "lives": user.lives,},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class GetLives(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='User ID',
                required=True
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'lives': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def get(self, request):
        user_id = request.query_params.get('user_id')
        user = User.objects.filter(user_id=user_id).first()
        if user:
            return Response({"username": user.username,"lives": user.lives}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'lives'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='User ID'),
                'lives': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of lives')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'lives': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        lives = request.data.get('lives')
        if lives < 0 or lives > 15:
            return Response({"error": "Lives must be between 0 and 15"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(user_id=user_id).first()
        if user:
            user.lives = lives
            user.save()
            return Response({"username": user.username, "lives": user.lives}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)