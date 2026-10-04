from decimal import Decimal

from susiturkki.domain.errors import RuleError

ONE_DECIMAL = Decimal("0.1")


def parse_distance_tenths(kilometers: Decimal) -> int:
    one_decimal = kilometers.quantize(ONE_DECIMAL)
    if one_decimal != kilometers:
        raise RuleError("distance_precision")
    if one_decimal <= 0:
        raise RuleError("distance_not_positive")
    return int(one_decimal * 10)


def optional_tenths(kilometers: Decimal | None) -> int | None:
    if kilometers is None:
        return None
    return parse_distance_tenths(kilometers)


def kilometers_from_tenths(tenths: int) -> Decimal:
    return (Decimal(tenths) / Decimal(10)).quantize(ONE_DECIMAL)
