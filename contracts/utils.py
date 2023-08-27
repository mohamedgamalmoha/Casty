

def get_model_field_names(model, exclude=None):
    """Get field names from model instance."""
    if exclude is None:
        exclude = []
    return list(filter(
        lambda field_name: field_name not in exclude,
        map(lambda field: field.name, model._meta.get_fields())
    ))
