from typing import Optional
import re

#################################### Validation Helper Functions #############################################################
def validate_email(email: Optional[str]) -> Optional[str]:
    if not email:
        return None

    email_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
        r'|^"([^\\"]|\\.)+"'
        r')@([A-Z0-9-]+\.)+[A-Z]{2,}$', re.IGNORECASE)

    if re.match(email_regex, email):
        return email
    else:
        return "invalid"

def validate_phone(phone: Optional[str]) -> Optional[str]:
    if not phone:
        return None

    phone = phone.replace(" ", "").replace("-", "")

    patterns = [
        r'^\+880\d{10}$',  # +880XXXXXXXXXX
        r'^0\d{10}$',       # 0XXXXXXXXXX
        r'^880\d{10}$'      # 880XXXXXXXXXX
    ]

    if any(re.match(pattern, phone) for pattern in patterns):
        return phone
    else:
        return "invalid"

#################################################################################################  