from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.employee import Employee
from app.schemas.employee import Employee as EmployeeSchema, EmployeeCreate, EmployeeUpdate

router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"]
)

@router.post("/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Crear un nuevo empleado"""
    # Verificar si el email ya existe
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el employee_id ya existe
    db_employee = db.query(Employee).filter(Employee.employee_id == employee.employee_id).first()
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de empleado ya existe"
        )
    
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/", response_model=list[EmployeeSchema])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de empleados"""
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=EmployeeSchema)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Obtener un empleado por ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    return employee

@router.put("/{employee_id}", response_model=EmployeeSchema)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    """Actualizar un empleado"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    
    update_data = employee.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Eliminar un empleado (desactivar)"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    
    db_employee.is_active = False
    db.commit()
    return None
