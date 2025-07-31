import secrets
import string


class CouponCodeGenerator:
    def generate(self, length: int = 10) -> str:
        alphabet = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))
