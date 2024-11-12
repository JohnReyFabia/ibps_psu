from django import template
from burnout_assessment.models import College  # Import your Schedule model

register = template.Library()

@register.simple_tag
def get_all_college():
    return College.objects.values('id', 'code', 'college_name', 'is_assessment_enabled').distinct().order_by('id')

