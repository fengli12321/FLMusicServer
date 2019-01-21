from django.utils.deprecation import MiddlewareMixin

class customMiddleware(MiddlewareMixin):

    def process_response(self, request, response):

        status_code = response.status_code
        success = status_code in range(200, 210)
        if response is not None:
            if success:
                response.data["data"] = response.data
                response.data["code"] = 1
            else:
                keys = []
                for key in response.data.keys():
                    keys.append(key)

                for key in keys:

                    print(key, response.data[key])
                    if isinstance(response.data[key], list):
                        response.data = {
                            'msg': response.data[key][0],
                            'code': -1
                        }
                    else:
                        response.data = {
                            "msg": response.data[key],
                            "code": -1
                        }
                    break

        else:
            if success:
                response.data = {
                    "code": 1,
                    "msg": "success",
                    "data": []
                }
            else:
                response.data = {
                    "code": -1,
                    "msg": "--其他错误--"
                }

        return response

