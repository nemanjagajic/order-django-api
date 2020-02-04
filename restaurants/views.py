from django.http import HttpResponse
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from restaurants.models import Restaurant, Food
from restaurants.serializers import RestaurantSerializer, FoodSerializer


class RestaurantViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (AllowAny,)


class FoodViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (AllowAny,)


class RestaurantFoodsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, id):
        try:
            restaurant = Restaurant.objects.prefetch_related('foods').get(pk=id)
            return HttpResponse(restaurant.foods.all(), content_type='application/json')
        except (Restaurant.DoesNotExist,):
            return Response({'error': 'There is no restaurant with provided id'},
                            status=status.HTTP_404_NOT_FOUND)
