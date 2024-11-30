def get_incomplete_fields(user):
    required_fields = {
        'age': 'Age',
        'location': 'Location',
        'personality_type': 'Personality Type',
        'available_time': 'Available Time',
        'budget_preference': 'Budget Preference'
    }
    
    incomplete = []
    for field, display_name in required_fields.items():
        if not getattr(user, field):
            incomplete.append(display_name)
    
    return incomplete