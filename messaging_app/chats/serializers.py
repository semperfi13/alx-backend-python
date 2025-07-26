from rest_framework import serializers
from .models import User, Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UserParticiapantsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name')
        read_only_fields = ['id', 'email', 'username', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    # sender info as consider as send id
    sender_info = UserParticiapantsSerializer(source='sender_id', read_only=True)
    message_summary = serializers.CharField(read_only=True)
    # OPTIONAL BECAUSE I HAVE ALREADY sender_info
    message_info = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_info',
            'sender_id',
            'conversation_id',
            'message_body',
            'message_info',
            'sent_at',
            'message_summary'
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender_info']

    def get_message_summary(self, obj):
        return f"{self.sender_info.full_name}: {obj.message_body[:50]}{'...' if len(obj.message_body) > 50 else ''}"

    def get_message_info(self, obj):
        return f"Message from {self.sender_info.full_name}: {obj.message_info}"

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError('Message body cannot be empty')
        if len(value) < 3:
            raise serializers.ValidationError('Message body must be at least 3 characters')
        return value


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserParticiapantsSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            'participants_id',
            'participants',
            'messages',
            'message_count',
            'subject',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['conversation_id', 'participants_id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def create(self, validated_data):
        conversation = Conversation.objects.create(**validated_data)
        return conversation
