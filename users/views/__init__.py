from .auth import (
    login_view as login,
    register_view as register,
    logout_view as logout,
    password_reset,
    new_password,
)
from .profile import profile
from .email import unverified_email, verify_email
from .account_settings import settings
