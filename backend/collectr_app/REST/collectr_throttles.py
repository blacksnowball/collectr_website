from rest_framework import throttling


class Relaxed(throttling.UserRateThrottle):
    scope = 'user_normal'
    rate = '500/min'


class Medium(throttling.UserRateThrottle):
    scope = 'user_post_trades'
    rate = '60/day'

    # def allow_request(self, request, view):
    #     if request.method == "POST":
    #         return True
    #     return super().allow_request()


class Stricter(throttling.UserRateThrottle):
    scope = 'user_post_requests'
    rate = '20/day'


class Strictest(throttling.UserRateThrottle):
    scope = 'user_post_requests'
    rate = '5/day'
