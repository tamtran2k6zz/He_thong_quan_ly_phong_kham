from backend.app.api.deps import (
    get_db,
    get_current_user,
    get_current_active_user,
    require_admin,
    require_receptionist,
    require_doctor,
    require_accountant,
    require_clinical_staff,
    require_all_staff
)

__all__ = [
    "get_db",
    "get_current_user",
    "get_current_active_user",
    "require_admin",
    "require_receptionist",
    "require_doctor",
    "require_accountant",
    "require_clinical_staff",
    "require_all_staff"
]
