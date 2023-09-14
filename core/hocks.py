

def postprocessing_exclude_stats_path(result, generator, request, public):
    """Exclude stats paths & components based on user role.
    Exclude them in case of being on-admin user. The only allowed users are staff and super ones.
    """
    is_staff_user = lambda user: user.is_superuser or user.is_staff
    if not is_staff_user(request.user):
        # Exclude paths in case of starting with /api/stats/
        result['paths'] = {path: value for path, value in result['paths'].items() if not path.startswith('/api/stats/')}
        # Exclude schemas in case of ending with Stats
        result['components'] = {schema: value for schema, value in result['components']['schemas'].items()
                                if schema.endswith('Stats')}
    return result
