from rest_framework import serializers
from .models import Smart, Category, Rating, Comment, Like
from django.db.models import Avg 


class LaptopSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Smart
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError('Количетсво не может быть отрицательным')
        return quantity

    def validate(self, attrs):
        