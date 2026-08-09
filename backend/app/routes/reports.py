from fastapi import APIRouter

from app.services.finance_service import finance_service
from app.services.inventory_service import inventory_service
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
def get_reports():
    return {"success": True, "report": report_service.generate_dashboard_report()}


@router.get("/today")
def today_report():
    return {"success": True, "report": finance_service.get_summary(today_only=True)}


@router.get("/low-stock")
def low_stock_report():
    products = inventory_service.get_low_stock_products()
    return {"success": True, "count": len(products), "products": products}


@router.get("/sales")
def sales_report():
    return {"success": True, "data": finance_service.get_summary()}


@router.get("/inventory")
def inventory_report():
    return {
        "success": True,
        "data": report_service.generate_dashboard_report()["inventory"],
    }


@router.get("/finance")
def finance_report():
    return {"success": True, "data": finance_service.get_summary()}
