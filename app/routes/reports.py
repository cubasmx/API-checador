from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database.database import get_db
from app.models.check_in import CheckIn
from app.models.employee import Employee

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"]
)

@router.get("/employee/{employee_id}/daily")
def get_daily_report(
    employee_id: int,
    date: str = None,
    db: Session = Depends(get_db)
):
    """Obtener reporte diario de un empleado"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    
    if not date:
        date = datetime.now().date()
    else:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    check_ins = db.query(CheckIn).filter(
        CheckIn.employee_id == employee_id,
        func.date(CheckIn.check_in_time) == date
    ).all()
    
    total_hours = 0
    for check_in in check_ins:
        if check_in.check_out_time:
            hours = (check_in.check_out_time - check_in.check_in_time).total_seconds() / 3600
            total_hours += hours
    
    return {
        "employee_id": employee_id,
        "employee_name": employee.name,
        "date": date,
        "check_ins": check_ins,
        "total_hours": round(total_hours, 2)
    }

@router.get("/employee/{employee_id}/monthly")
def get_monthly_report(
    employee_id: int,
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db)
):
    """Obtener reporte mensual de un empleado"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    check_ins = db.query(CheckIn).filter(
        CheckIn.employee_id == employee_id,
        func.extract('year', CheckIn.check_in_time) == year,
        func.extract('month', CheckIn.check_in_time) == month
    ).all()
    
    total_hours = 0
    for check_in in check_ins:
        if check_in.check_out_time:
            hours = (check_in.check_out_time - check_in.check_in_time).total_seconds() / 3600
            total_hours += hours
    
    return {
        "employee_id": employee_id,
        "employee_name": employee.name,
        "year": year,
        "month": month,
        "total_check_ins": len(check_ins),
        "total_hours": round(total_hours, 2)
    }

@router.get("/department/{department}")
def get_department_report(
    department: str,
    date: str = None,
    db: Session = Depends(get_db)
):
    """Obtener reporte diario de un departamento"""
    if not date:
        date = datetime.now().date()
    else:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    employees = db.query(Employee).filter(Employee.department == department).all()
    
    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Departamento no encontrado"
        )
    
    report_data = []
    for employee in employees:
        check_ins = db.query(CheckIn).filter(
            CheckIn.employee_id == employee.id,
            func.date(CheckIn.check_in_time) == date
        ).all()
        
        total_hours = 0
        for check_in in check_ins:
            if check_in.check_out_time:
                hours = (check_in.check_out_time - check_in.check_in_time).total_seconds() / 3600
                total_hours += hours
        
        report_data.append({
            "employee_id": employee.id,
            "employee_name": employee.name,
            "total_hours": round(total_hours, 2),
            "check_count": len(check_ins)
        })
    
    return {
        "department": department,
        "date": date,
        "employees": report_data
    }
