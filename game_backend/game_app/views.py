from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Reward
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetScoreboard(APIView):
    def get(self, request):
        users = User.objects.order_by('-high_score')[:100]
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
            return Response({"user_id": user.user_id, "last_game_score": user.last_game_score,"high_score": user.high_score, "lipathToGloryLivesves": user.pathToGloryLives, "arcticFortuneLives": user.arcticFortuneLives}, status=status.HTTP_200_OK)
        else:
            user = User.objects.create(user_id=user_id, username=username, last_game_score=last_game_score, high_score=last_game_score, pathToGloryLives=0,arcticFortuneLives=0)
            return Response({"user_id": user.user_id, "last_game_score": user.last_game_score,"high_score": user.high_score, "lipathToGloryLivesves": user.pathToGloryLives, "arcticFortuneLives": user.arcticFortuneLives}, status=status.HTTP_201_CREATED)
    

class GetUser(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description='User ID',
                required=True
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_game_score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'high_score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'pathToGloryLives': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'arcticFortuneLives': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'investment': openapi.Schema(type=openapi.TYPE_NUMBER)
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
    def get(self, request, user_id):
        user = User.objects.filter(user_id=user_id).first()

        if user:
            return Response({"user_id": user.user_id, 
                            "username": user.username,
                            "last_game_score": user.last_game_score,
                            "high_score": user.high_score,
                            "arcticFortuneLives": user.arcticFortuneLives,
                            "pathToGloryLives": user.pathToGloryLives,
                            "investment": user.investment,},
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
                    'pathToGloryLives': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'arcticFortuneLives': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'investment': openapi.Schema(type=openapi.TYPE_NUMBER)
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
            return Response({"username": user.username,"pathToGloryLives": user.pathToGloryLives, "arcticFortuneLives": user.arcticFortuneLives , "investment": user.investment}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'lives'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='User ID'),
                'pathToGloryLives': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of Path to Glory lives'),
                'arcticFortuneLives': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of Arctic Fortune lives'),
                'investment': openapi.Schema(type=openapi.TYPE_NUMBER, description='Investment amount')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'pathToGloryLives': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of Path to Glory lives'),
                    'arcticFortuneLives': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of Arctic Fortune lives'),
                    'investment': openapi.Schema(type=openapi.TYPE_NUMBER)
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
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
        arcticFortuneLives = request.data.get('arcticFortuneLives')
        pathToGloryLives = request.data.get('pathToGloryLives')
        investment = request.data.get('investment')
        user = User.objects.filter(user_id=user_id).first()
        if user:
            if arcticFortuneLives is not None:
                if arcticFortuneLives < 0 or arcticFortuneLives > 15:
                    return Response({"error": "arcticFortuneLives must be between 0 and 15"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.arcticFortuneLives = arcticFortuneLives
            if pathToGloryLives is not None:
                if pathToGloryLives < 0 or pathToGloryLives > 15:
                    return Response({"error": "pathToGloryLives must be between 0 and 15"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.pathToGloryLives = pathToGloryLives
            user.investment = investment
            user.save()
            return Response({"username": user.username, "arcticFortuneLives": user.arcticFortuneLives, "pathToGloryLives": user.pathToGloryLives, "investment": user.investment}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class GetReward(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'wallet_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'score': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'mode': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def get(self, request):
        rewards = Reward.objects.all()[:100]
        return Response(rewards.values('wallet_id', 'score', 'amount', 'mode'), status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['wallet_id', 'score', 'amount', 'mode'],
            properties={
                'wallet_id': openapi.Schema(type=openapi.TYPE_STRING, description='Wallet ID'),
                'score': openapi.Schema(type=openapi.TYPE_INTEGER, description='User score'),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Reward amount'),
                'mode': openapi.Schema(type=openapi.TYPE_STRING, description='Game mode')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'wallet_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'mode': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'wallet_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'mode': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request):
        wallet_id = request.data.get('wallet_id')
        amount = request.data.get('amount')
        score = request.data.get('score')
        mode = request.data.get('mode')
        user = Reward.objects.filter(wallet_id=wallet_id).first()
        if user:
            user.score = score
            user.amount = amount
            user.mode = mode
            user.save()
            return Response({"wallet_id": user.wallet_id, "score": user.score,"amount": user.amount, "mode": user.mode}, status=status.HTTP_200_OK)
        else:
            user = Reward.objects.create(wallet_id=wallet_id, score=score, amount=amount, mode=mode)
            return Response({"wallet_id": user.wallet_id, "score": user.score,"amount": user.amount, "mode": user.mode}, status=status.HTTP_201_CREATED)