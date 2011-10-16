

class CustomFunctionLoopError(Exception):
    """ A custom_mutator or a custom_accessor calls get_field_value or
        set_field_value again without using override, thus causing an
        infinite loop.
        This error is raised when this behaviour is detected, to stop
        execution.
    """
