from rest_framework import serializers

from app_report.models import ApiCppTable,ApiJavaTable,PluginTalbe,ServerTalbe


class ApiCppTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiCppTable
        fields = '__all__'

class ApiJavaTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiJavaTable
        fields = '__all__'

class PluginTalbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginTalbe
        fields = '__all__'

class ServerTalbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerTalbe
        fields = '__all__'