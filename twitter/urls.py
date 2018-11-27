from django.conf.urls import url, include
from rest_framework.permissions import AllowAny 
from twitter.users.views import UserViewSet, GroupViewSet, UserTweetsViewSet
from twitter.tweets.views import TweetViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter


router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'tweets', TweetViewSet)

users_router = NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'tweets', UserTweetsViewSet, base_name='user-tweets')

schema_view = get_schema_view(
   openapi.Info(
      title="Twitter Clone API",
      default_version='v1',
      description="RESTful API for a simple Twitter clone",
      terms_of_service="https://developer.twitter.com/en/developer-terms/agreement-and-policy.html",
      contact=openapi.Contact(email="fabio.maia@fer.hr"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(AllowAny,),
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Resources
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(users_router.urls)),

    # Token
    url(r'^api/token$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/token/verify$', TokenVerifyView.as_view(), name='token_verify'),

    # Documentation
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
