class PaymentDomainError(Exception):
    pass


class GatewayTokenError(Exception):
    pass


class GatewayRequestError(Exception):
    pass


class GatewayTimeoutError(Exception):
    pass
