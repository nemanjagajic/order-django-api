from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=225)
    location = models.CharField(max_length=225)

    def __str__(self):
        return self.name + ', ' + self.location


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='foods', on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    price = models.CharField(max_length=225)

    def __str__(self):
        return self.name + ' ' + self.price + '\n'


class Order(models.Model):
    user = models.ForeignKey('users.User', related_name='orders', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    foods = models.ManyToManyField(Food, blank=False, related_name='order_foods', through='OrderFood')
    status = models.CharField(max_length=225, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.id) + ' ' + self.user.username + ' ' + self.restaurant.name + '\n'


class OrderFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
