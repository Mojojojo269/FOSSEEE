from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_timestamp', 'summary_json', 'csv_path', 'user']
        read_only_fields = ['id', 'upload_timestamp', 'user']
