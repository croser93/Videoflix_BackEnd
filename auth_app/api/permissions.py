from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
class CookieJWTAuth(JWTAuthentication):
    """
    Authenticate requests using the JWT access token stored in the
    'access_token' cookie instead of the Authorization header.

    Returns None if no access token cookie is present (falls through to
    other authentication classes), otherwise returns (user, validated_token).
    """

    def authenticate(self, request):
        access = request.COOKIES.get('access_token')
        
        if access is None:
            return None
        try:
            validated = self.get_validated_token(access)
            user = self.get_user(validated_token = validated)
            return (user, validated)
        except (InvalidToken, TokenError):
            return None 
