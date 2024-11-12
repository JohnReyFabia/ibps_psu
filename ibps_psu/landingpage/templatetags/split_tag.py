from django import template

register = template.Library()

@register.filter
def first_sentence(text):
    # Find the position of the first period
    period_position = text.find('.')
    
    # Check if a period was found
    if period_position != -1:
        # Include the period in the first sentence
        first_sentence = text[:period_position + 1]
    else:
        # If no period is found, return the entire text
        first_sentence = text
    
    return first_sentence
