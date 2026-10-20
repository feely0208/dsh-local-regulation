def mask_phone(value: str) -> str:
    """手机号掩码：保留前三后四。"""
    if not value:
        return value
    return value[:3] + "****" + value[-4:]


def mask_id_card(value: str) -> str:
    """身份证号掩码：保留前六后二。"""
    if not value:
        return value
    return value[:6] + "*" * (len(value) - 8) + value[-2:]
