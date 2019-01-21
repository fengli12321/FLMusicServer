from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:

        keys = []
        for key in response.data.keys():
            keys.append(key)

        for key in keys:

            print(key, response.data[key])
            if isinstance(response.data[key], list):
                response.data[key] = response.data[key][0]

    return response