from typing import List, Tuple

from django.utils.decorators import classonlymethod

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, SAFE_METHODS


class RetrieveMethodNotAllowedMixin:
    """Raise an exception to deny GET request to get a specific object by ID"""

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class ListMethodNotAllowedMixin:
    """Raise an exception to deny GET request to get a list of objects"""

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class PutMethodNotAllowedMixin:
    """Raise an exception to deny PUT request to update a specific object by ID"""

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class PatchMethodNotAllowedMixin:
    """Raise an exception to deny PATCH request to partially update a specific object by ID"""

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class UpdateMethodNotAllowedMixin(PutMethodNotAllowedMixin, PatchMethodNotAllowedMixin):
    """Raise an exception to deny PATCH / PUT request to update a specific object by ID"""
    ...


class CreateMethodNotAllowedMixin:
    """Raise an exception to deny CREATE request to create a new object"""

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class DestroyMethodNotAllowedMixin:
    """Raise an exception to deny DELETE request to delete a specific object by ID"""

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class AllowAnyInSafeMethodOrCustomPermissionMixin:
    """
    Mixin to allow safe methods (GET, HEAD, OPTIONS) for any user,
    while applying permission classes for other methods.
    """
    save_method_permission_classes = [AllowAny]

    def get_permission_classes(self, request):
        if request.method in SAFE_METHODS:
            return self.save_method_permission_classes
        return super().get_permission_classes(request)


class ThrottleActionsWithMethodsMixin:
    """
    Mixin to allow throttling actions with http methods.
    In case of action and request method are existed in throttle_actions, the throttling is applied.
    EG.:
        [
            ('retrieve', 'GET'),
            ('update', 'PUT'),
            ...
        ]
    """
    throttle_actions: List[Tuple[str, str]] = []

    def get_throttles(self):
        if not ((self.action, self.request.method) in self.throttle_actions):
            return []
        return super().get_throttles()


class ProhibitedActionsMixin:
    """
    Mixin class to restrict specific actions in views.

    This Mixin provides a mechanism to filter out specific actions
    from being available in the view. The actions to be prohibited are
    defined in `prohibited_actions`.

    Attributes:
        - prohibited_actions (List[Tuple[str, str]]): A list of tuples where each tuple represents
            an action to be prohibited. By default, it's set to None which means no actions are prohibited.
            Each tuple consists of two strings:
                1. The HTTP method in lowercase (e.g., 'get', 'post').
                2. The corresponding view function name (e.g., 'list', 'create').
            An example tuple might be `('get', 'list')`, where 'get' is the HTTP method and
            'list' is the name of the view function.

    Methods:
        as_view: Filters out the prohibited actions from the view and then calls the `as_view`
            method of the super class.
    """

    prohibited_actions: List[Tuple[str, str]] = None

    @classmethod
    def as_view(cls, actions=None, **initkwargs):
        """
        Overrides the as_view method to filter out the prohibited actions.

        If `prohibited_actions` is defined, this method filters out the prohibited actions
        from the provided `actions` dictionary and then calls the `as_view` method of the super class.

        Args:
            actions (dict, optional): A dictionary of actions. Defaults to None.
            **initkwargs: Arbitrary keyword arguments.

        Returns:
            function: The view function after filtering the prohibited actions.
        """
        if cls.prohibited_actions is not None:
            actions = dict(filter(lambda item: item not in cls.prohibited_actions, actions.items()))
        return super().as_view(actions, **initkwargs)
