from rest_framework import throttling

class anonRelaxed(throttling.AnonRateThrottle):
    scope='anon_relaxed'
    rate = '300/min'


class anonStricter(throttling.AnonRateThrottle):
    scope = 'anon_stricter'
    rate = '20/min'


class anonStrictest(throttling.AnonRateThrottle):
    scope = 'anon_strictest'
    rate = '5/min'


class userNormal(throttling.UserRateThrottle):
    scope = 'user_normal'
    rate = '500/min'