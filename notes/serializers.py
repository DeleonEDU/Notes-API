from rest_framework import serializers

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