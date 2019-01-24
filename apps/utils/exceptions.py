from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:

        keys = []
        for key in response.data:
            keys.append(key)

        errors = []
        for key in keys:
            if isinstance(response.data[key], list):
                for error in response.data[key]:
                    errors.append(error)
                del response.data[key]
        response.data["error"] = ", ".join(errors)
    return response

