from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Student, Professor, Module, Rating



class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'password']


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'



class ModuleSerializer(serializers.ModelSerializer):
    # Custom field for professor names
    professors = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'module_code', 'name', 'year', 'semester', 'professors']

    def get_professors(self, obj):
        # Return a list of professor names
        return [prof.name for prof in obj.professor.all()]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
