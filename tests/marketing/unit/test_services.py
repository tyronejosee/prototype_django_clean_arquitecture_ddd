from src.modules.marketing.domain.services.coupon_code_generator import CouponCodeGenerator


class TestCouponCodeGenerator:
    def test_should_generate_default_length_code(self) -> None:
        generator = CouponCodeGenerator()

        # When: generating a code of default length
        code = generator.generate()

        # Then: should be 10 characters long
        assert len(code) == 10
        assert code.isupper()
        assert code.isalnum()

    def test_should_generate_code_with_custom_length(self) -> None:
        generator = CouponCodeGenerator()

        # When: generating a code of 16 characters
        code = generator.generate(length=16)

        # Then: should match length and be alphanumeric
        assert len(code) == 16
        assert all(c.isupper() or c.isdigit() for c in code)
