from django.db import transaction
from django.http import HttpResponse
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from restaurants.models import Restaurant, Food, Order
from restaurants.serializers import RestaurantSerializer, FoodSerializer


class RestaurantViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)


class FoodViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)


class RestaurantFoodsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            restaurant = Restaurant.objects.prefetch_related('foods').get(pk=id)
            return HttpResponse(restaurant.foods.all(), content_type='application/json')
        except (Restaurant.DoesNotExist,):
            return Response({'error': 'There is no restaurant with provided id'},
                            status=status.HTTP_404_NOT_FOUND)


class OrderFoodAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        try:
            with transaction.atomic():
                restaurant = Restaurant.objects.prefetch_related('foods').get(pk=id)
                order = Order.objects.create(user_id=request.user.id, restaurant_id=restaurant.id)

                food_ids = json.loads(request.body)['food_ids']

                for food_id in food_ids:
                    food = Food.objects.get(pk=food_id, restaurant_id=restaurant.id)
                    order.foods.add(food)

                return HttpResponse('Successfully created order with id ' + str(order.id),
                                    status=status.HTTP_201_CREATED)
        except (Restaurant.DoesNotExist,):
            return Response({'error': 'There is no restaurant with provided id'},
                            status=status.HTTP_404_NOT_FOUND)
        except (Food.DoesNotExist,):
            return Response({'error': 'There is no food with provided id in given restaurant'},
                            status=status.HTTP_404_NOT_FOUND)
