from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from oauth.serializers import GitHubAuthSerializer

class GitHubAuthView(APIView):
    def post(self, request):
        serializer = GitHubAuthSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            response = requests.post(
                'https://github.com/login/oauth/access_token',
                headers={
                    'Accept': 'application/json',  # Ask for the response in JSON format
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                data={
                    'client_id': data['client_id'],
                    'client_secret': data['client_secret'],
                    'code': data['code'],
                    'redirect_uri': settings.GITHUB_REDIRECT_URL,
                },
            )

            response_json = response.json()
            if response_json.get('error') == 'redirect_uri_mismatch':
                # If the error is 'redirect_uri_mismatch', try again with a different redirect_uri
                response = requests.post(
                    'https://github.com/login/oauth/access_token',
                    headers={
                        'Accept': 'application/json',
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    data={
                        'client_id': data['client_id'],
                        'client_secret': data['client_secret'],
                        'code': data['code'],
                        'redirect_uri': 'http://localhost:5173/auth/github',
                    },
                )

            # Handle the response from either the first or second request
            if response.status_code == 200:
                return Response(response.json(), status=200)
            else:
                return Response({'details': 'Failed to retrieve access token'}, status=response.status_code)
