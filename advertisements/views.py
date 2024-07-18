from shared_imports import *


# Create your views here.
class AdvertisementViewSet(generics.ListAPIView):
    queryset = Advertisement.objects.all().order_by('-priority', '-created_at')
    serializer_class = AdvertisementSerializer
    permission_classes = []  