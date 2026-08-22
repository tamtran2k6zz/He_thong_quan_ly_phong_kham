from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.database import get_db
from backend.app.models.prescription import Medicine
from backend.app.models.audit import AuditLog
from backend.app.models.user import User
from backend.app.schemas.prescription import (
    MedicineCreate,
    MedicineUpdate,
    MedicineResponse
)
from backend.app.api.deps import require_admin, require_all_staff

router = APIRouter(prefix="/medicines", tags=["Medicines Management"])


def generate_medicine_code(db: Session, name: str) -> str:
    """Generates unique medicine code in format MED-NAME-XXXX or MED-YYYYMMDD-XXXX."""
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"MED-{today_str}-"
    count = db.query(Medicine).filter(Medicine.code.like(f"{prefix}%")).count()
    candidate = f"{prefix}{count + 1:04d}"
    while db.query(Medicine).filter(Medicine.code == candidate).first():
        count += 1
        candidate = f"{prefix}{count + 1:04d}"
    return candidate


@router.get("", response_model=List[MedicineResponse])
def get_medicines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    q: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Search and list medicines catalog.
    Supports filtering by name, active ingredient, or code.
    """
    query = db.query(Medicine)
    if is_active is not None:
        query = query.filter(Medicine.is_active == is_active)
    if q:
        search_filter = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Medicine.name.ilike(search_filter),
                Medicine.active_ingredient.ilike(search_filter),
                Medicine.code.ilike(search_filter)
            )
        )
    return query.order_by(Medicine.name.asc()).offset(skip).limit(limit).all()


@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Get medicine details by ID.
    """
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thông tin thuốc"
        )
    return medicine


@router.post("", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(
    medicine_in: MedicineCreate,
    request: Request,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Create a new medicine in the catalog (Admin only).
    """
    code = medicine_in.code
    if not code:
        code = generate_medicine_code(db, medicine_in.name)
    else:
        existing = db.query(Medicine).filter(Medicine.code == code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã thuốc '{code}' đã tồn tại trong danh mục"
            )

    med_data = medicine_in.model_dump(exclude_unset=False)
    med_data["code"] = code

    medicine = Medicine(**med_data)
    db.add(medicine)
    db.commit()
    db.refresh(medicine)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=admin_user.id,
        action="CREATE_MEDICINE",
        resource_type="Medicine",
        resource_id=str(medicine.id),
        details=f"Created medicine {medicine.name} ({medicine.code}) by {admin_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return medicine


@router.put("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    medicine_in: MedicineUpdate,
    request: Request,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Update medicine details or restock quantity (Admin only).
    """
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thông tin thuốc"
        )

    update_data = medicine_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medicine, field, value)

    db.commit()
    db.refresh(medicine)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=admin_user.id,
        action="UPDATE_MEDICINE",
        resource_type="Medicine",
        resource_id=str(medicine.id),
        details=f"Updated medicine {medicine.name} ({medicine.code}) by {admin_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return medicine


@router.delete("/{medicine_id}", status_code=status.HTTP_200_OK)
def delete_medicine(
    medicine_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Deactivate or delete medicine (Admin only).
    """
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thông tin thuốc"
        )

    # Deactivate or delete
    db.delete(medicine)
    db.commit()

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=admin_user.id,
        action="DELETE_MEDICINE",
        resource_type="Medicine",
        resource_id=str(medicine_id),
        details=f"Deleted medicine ID {medicine_id} by {admin_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return {"message": f"Đã xóa thuốc thành công"}
