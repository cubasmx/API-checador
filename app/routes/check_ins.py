from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.database import get_db
from app.models.check_in import CheckIn
from app.models.employee import Employee
from app.schemas.check_in import CheckIn as CheckInSchema, CheckInCreate, CheckOutCreate

router = APIRouter(
    prefix="/api/v1/check-ins",
    tags=["Check-Ins"]
)

@router.post("/check-in", response_model=CheckInSchema, status_code=status.HTTP_201_CREATED)
def check_in(check_in: CheckInCreate, db: Session = Depends(get_db)):
    """Registrar entrada de un empleado"""
    # Verificar que el empleado existe
    employee = db.query(Employee).filter(Employee.id == check_in.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    
    if not employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El empleado está inactivo"
        )
    
    # Verificar si el empleado ya tiene una entrada sin salida
    active_check_in = db.query(CheckIn).filter(
        CheckIn.employee_id == check_in.employee_id,
        CheckIn.check_out_time.is_(None)
    ).first()
    
    if active_check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El empleado ya tiene una entrada sin salida"
        )
    
    new_check_in = CheckIn(
        employee_id=check_in.employee_id,
        check_in_time=datetime.now(),
        notes=check_in.notes
    )
    db.add(new_check_in)
    db.commit()
    db.refresh(new_check_in)
    return new_check_in

@router.post("/{check_in_id}/check-out", response_model=CheckInSchema)
def check_out(check_in_id: int, check_out: CheckOutCreate, db: Session = Depends(get_db)):
    """Registrar salida de un empleado"""
    db_check_in = db.query(CheckIn).filter(CheckIn.id == check_in_id).first()
    if not db_check_in:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de entrada no encontrado"
        )
    
    if db_check_in.check_out_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este registro ya tiene una salida registrada"
        )
    
    db_check_in.check_out_time = datetime.now()
    if check_out.notes:
        db_check_in.notes = check_out.notes
    
    db.commit()
    db.refresh(db_check_in)
    return db_check_in

@router.get("/", response_model=list[CheckInSchema])
def get_check_ins(
    employee_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener registros de entrada/salida"""
    query = db.query(CheckIn)
    
    if employee_id:
        query = query.filter(CheckIn.employee_id == employee_id)
    
    check_ins = query.offset(skip).limit(limit).all()
    return check_ins

@router.get("/{check_in_id}", response_model=CheckInSchema)
def get_check_in(check_in_id: int, db: Session = Depends(get_db)):
    """Obtener un registro de entrada/salida"""
    check_in = db.query(CheckIn).filter(CheckIn.id == check_in_id).first()
    if not check_in:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado"
        )
    return check_in
