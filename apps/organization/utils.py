from django.core import signing
from django.utils import timezone
from datetime import timedelta

def generate_invite_token(sender_id, org_id,invited_member_username, expiration_minutes=6000):
    data = {
        "sender_id": str(sender_id),
        "org_id": str(org_id),
        "exp": (timezone.now() + timedelta(minutes=expiration_minutes)).timestamp(),
        "invited_username": invited_member_username,
    }
    token = signing.dumps(data)
    return token

def verify_invite_token(token):
    try:
        data = signing.loads(token)
        if timezone.now().timestamp() > data["exp"]:
            raise ValueError("Token expired")
        return data
    except signing.BadSignature:
        raise ValueError("Invalid token")
