import re

def validate_uz_phone_number(phone: str) -> bool:
    """
    O'zbekiston mobil telefon raqamini tekshiradi.
    Format: +998XXYYYYYYY yoki 998XXYYYYYYY (XX - operator kodi, YYYYYYY - 7 raqam)
    Qabul qilinadigan operator kodlari: 33, 88, 90, 91, 93, 94, 95, 97, 98, 99
    """
    phone = phone.replace(" ", "").replace("-", "")

    pattern = r'^(?:\+998|998)(20|33|50|55|70|77|87|88|90|91|93|94|95|97|98|99)\d{7}$'

    return bool(re.match(pattern, phone))