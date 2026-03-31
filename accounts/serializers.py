from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.text import slugify
from shops.models import Shop


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    shop_name = serializers.CharField(max_length=200)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        shop_name = validated_data['shop_name']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )

        # Generate a unique slug from the shop name
        base_slug = slugify(shop_name)
        slug = base_slug
        counter = 1
        while Shop.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Shop.objects.create(owner=user, slug=slug, name=shop_name)
        return user
