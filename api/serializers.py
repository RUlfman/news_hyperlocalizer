from rest_framework import serializers
from .models import Source, Story, Label
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class ObtainAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                token, _ = Token.objects.get_or_create(user=user)
                attrs['token'] = token.key
                return attrs
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all(), required=False)

    class Meta:
        model = Story
        fields = '__all__'

    def update(self, instance, validated_data):
        labels_data = validated_data.pop('labels')
        instance = super().update(instance, validated_data)

        # Clear existing labels
        instance.labels.clear()

        # Add new labels
        for label in labels_data:
            instance.labels.add(label)

        return instance

class ObtainAuthTokenResponseSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField()


