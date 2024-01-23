from rest_framework import serializers

class GitHubAuthSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    client_secret = serializers.CharField()
    code = serializers.CharField()
    redirect_uri = serializers.CharField()