from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth import get_user_model
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    # permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'star' in request.data:

            movie = Movie.objects.get(id=pk)
            star = request.data['star']
            user = request.user
            # user = get_user_model().objects.get(id=1)
            print('user', user)
            print('movie', movie)
            print('star', star)
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.star = star
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message' : '평가가 업데이트 되었습니다.', 'result' : serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, star=star)
                serializer = RatingSerializer(rating, many=False)
                response = {'message' : '평가가 생성되었습니다.', 'result' : serializer.data}
                print(response)
                return Response(response, status=status.HTTP_200_OK)
            
        else:
            response = {'message' : 'You neeed to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )

    def create(self, request, *args, **kwargs):
        response = {'message' : '생성하는 방법이 잘못되었습니다'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        response = {'message' : '수정하는 방법이 잘못되었습니다'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)