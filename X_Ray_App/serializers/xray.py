from rest_framework import serializers
from X_Ray_App.models import XRay

class XRaySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, allow_null=False, use_url=False)

    class Meta:
        model = XRay
        fields = ('pk', 'image')
