from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


DEFAULT_SIZE = 5  # MB
MP_CONVERSION_RATE = 1048576


@deconstructible
class FileSizeValidator:
    """Validates the size of the file, the size limit is entered in MB.
    For example:
        - 2.5MB: 2621440
        - 5MB: 5242880
        - 10MB: 10485760
        - 20MB: 20971520
        - 50MB: 5242880
        - 100MB: 104857600
        - 250MB: 214958080
        - 500MB: 429916160
    """

    message = _('File size exceeds the limit of “%(max_size)” .')
    code = 'size_limit'
    fail_message = _(
        'Validation of file size is failed. '
        'It gives the following error “%(error)”'
    )
    fail_code = 'validation_fail'

    @property
    def size_limit_str(self):
        return f'{self.size_limit:.1f}MB'

    @property
    def size_limit_value(self):
        return self.size_limit * MP_CONVERSION_RATE

    def __init__(self, size_limit: int = DEFAULT_SIZE, message=None, code=None):
        self.size_limit = size_limit

        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        try:
            if value._size > self.size_limit_value:
                raise ValidationError(
                    self.message,
                    code=self.code,
                    params={
                        'max_size': self.size_limit_str,
                    }
                )
        except (AttributeError, ValueError) as e:
            raise ValidationError(
                self.fail_message,
                code=self.fail_code,
                params={
                    'error': e,
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.size_limit == other.size_limit and
            self.message == other.message and
            self.code == other.code and
            self.fail_message == other.fail_message,
            self.fail_code == other.fail_code
        )


@deconstructible
class FileContentTypeValidator:
    message = _(
        'File content type “%(content_type)s” is not allowed. '
        'Allowed content types are: %(allowed_types)s.'
    )
    code = 'invalid_type'
    fail_message = _(
        'Validation of file content is failed. '
        'It gives the following error “%(error)”'
    )
    fail_code = 'validation_fail'

    def __init__(self, allowed_types, message=None, code=None):
        self.allowed_types = allowed_types
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        try:
            if value.content_type not in self.allowed_types:
                raise ValidationError(
                    self.message,
                    code=self.code,
                    params={
                        'content_type': value.content_type,
                        'allowed_types': ', '.join(self.allowed_types),
                    }
                )
        except (AttributeError, ValueError) as e:
            raise ValidationError(
                self.fail_message,
                code=self.fail_code,
                params={
                    'error': e,
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.allowed_types == other.allowed_types and
            self.message == other.message and
            self.code == other.code and
            self.fail_message == other.fail_message,
            self.fail_code == other.fail_code
        )
