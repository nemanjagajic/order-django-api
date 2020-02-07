from django.db import transaction
from django.http import HttpResponse
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from restaurants.models import Restaurant, Food, Order, OrderFood
from restaurants.serializers import RestaurantSerializer, FoodSerializer
from users.models import User


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
            foods = restaurant.foods.all()
            foods_response = []
            for food in foods:
                foods_response.append({
                    'id': food.id,
                    'name': food.name,
                    'price': food.price,
                    'restaurant_id': food.restaurant_id
                })
            return HttpResponse(json.dumps(foods_response), content_type='application/json')
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

                order_foods = json.loads(request.body)['order_foods']

                for order_food in order_foods:
                    food = Food.objects.get(pk=order_food['food_id'], restaurant_id=restaurant.id)
                    of = OrderFood(food_id=food.id, order_id=order.id, count=order_food['count'])
                    of.save()

                return HttpResponse('Successfully created order with id ' + str(order.id),
                                    status=status.HTTP_201_CREATED)
        except (Restaurant.DoesNotExist,):
            return Response({'error': 'There is no restaurant with provided id'},
                            status=status.HTTP_404_NOT_FOUND)
        except (Food.DoesNotExist,):
            return Response({'error': 'There is no food with provided id in given restaurant'},
                            status=status.HTTP_404_NOT_FOUND)


class OrdersAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            orders = Order.objects.filter(user_id=request.user.id)
            orders_response = []
            for order in orders:
                restaurant = Restaurant.objects.get(pk=order.restaurant_id)
                orders_response.append({
                    'id': order.id,
                    'status': order.status,
                    'created_at': str(order.created_at),
                    'restaurant': {
                        'id': restaurant.location,
                        'name': restaurant.name,
                        'location': restaurant.location
                    }
                })
            return HttpResponse(json.dumps(orders_response), content_type='application/json')
        except (User.DoesNotExist,):
            return Response({'error': 'There is no user with provided id'},
                            status=status.HTTP_404_NOT_FOUND)
