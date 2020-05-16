import django_filters
from classroom.models import Quiz, Profile, Student, Capteur

class CasesFilter (django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = [ 'subject',]



class ExpertsFilter (django_filters.FilterSet):
    class Meta:
        model = Student
        fields = ['interests', 'domaine']






class CapteurFilter (django_filters.FilterSet):
    class Meta:
        model = Capteur
        fields = [ 'subject', 'domaine', 'technologie_utilisee', 'type_evt' ]





