from rest_framework import serializers
from django.utils.html import escape
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id',
            'title',
            'content',
            'owner',
            'created_at',
        ]
        read_only_fields = [
            'owner',
            'created_at'
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Title cannot be empty')
        return escape(value.strip())


    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError('Content cannot be empty')
        return escape(value.strip())
    

class NoteUpdateSerializer(NoteSerializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    