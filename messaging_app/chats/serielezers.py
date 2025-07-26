from rest_framework import serializers
from .models import User, Conversation, Message


class CustomUserSerializer(serializers.ModelSerializer):
    my_field = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return


class MessageSerializer(serializers.ModelSerializer):
    my_field = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        return


class ConversationSerializer(serializers.ModelSerializer):
    my_field = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'

    def create(self, validated_data):
        return
