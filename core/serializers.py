from rest_framework import serializers
from .models import Snippet, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model =Tag
        fields = '__all__'

class SnippetSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
    view_name='snippet-detail',
    lookup_field='pk'
)

    class Meta:
        model = Snippet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'user']
