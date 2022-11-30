from dataclasses import field
from rest_framework import serializers
from .models import Smart, Category, Rating, Comment, Like, SmartImage
from django.db.models import Avg 


class SmartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Smart
        exclude = ('slug', 'created_at', 'updated_at', 'category',)
        

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError('Количетсво не может быть отрицательным')
        return quantity

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user 
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(
            instance.comments.all(), many=True
        ).data
        rep['carousel'] = SmartImageSerializer(
            instance.smart_images.all(), many=True).data
        rating = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        rep['likes'] = instance.likes.all().count()
        rep['liked_by'] = LikeSerializer(
            instance.likes.all().only('user'), many=True).data
        if rating:
            rep['rating'] = round(rating, 1)
        else:
            rep['rating'] = 0.0
        return rep


class SmartListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Smart
        fields = ('image', 'title', 'price', 'in_stock',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comments.all().count()
        return rep


class SmartCreateSerilizer(serializers.ModelSerializer):
    carousel_img = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = Smart
        fields = '__all__'

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        smart = Smart.objects.create(**validated_data)
        images = []
        for image in carousel_images:
            images.append(SmartImage(smart=smart, image=image))
        SmartImage.objects.bulk_create(images)
        return smart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Comment
        exclude = ['smart']


class SmartImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartImage
        fields = 'image',


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        model = Rating
        fields = ('rating', 'user', 'smart',)

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating')
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError(
                'Wrong value! Rating must be between 1 and 5'
            )
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class CurrentSmartDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['smart']
        


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    smart = serializers.HiddenField(default=CurrentSmartDefault())

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        smart = self.context.get('smart').pk
        like = Like.objects.filter(user=user, smart=smart).first()
        if like:
            raise serializers.ValidationError('Already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        smart = self.context.get('smart').pk
        like = Like.objects.filter(user=user, smart=smart).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')