from rest_framework.authentication import TokenAuthentication


class ApiKeyAuthentication(TokenAuthentication):
    keyword = 'api-key'
