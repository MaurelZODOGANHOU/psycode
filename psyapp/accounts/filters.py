import django_filters
from .models import TypeConsultation


class TypeConsultationFilter(django_filters.FilterSet):
    type_name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = TypeConsultation
        fields = ['type_name']
