from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, RoleEnum
from backend.app.core.rbac import (
    get_current_user,
    get_current_active_user,
    require_roles,
    RoleChecker
)

# Common Role Checkers
require_admin = require_roles([RoleEnum.ADMIN])
require_receptionist = require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST])
require_doctor = require_roles([RoleEnum.ADMIN, RoleEnum.DOCTOR])
require_accountant = require_roles([RoleEnum.ADMIN, RoleEnum.ACCOUNTANT])
require_clinical_staff = require_roles([RoleEnum.ADMIN, RoleEnum.DOCTOR, RoleEnum.RECEPTIONIST])
require_all_staff = require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.DOCTOR, RoleEnum.ACCOUNTANT])
