from fastapi import APIRouter

router = APIRouter()


@router.get("/reports")
def get_reports():
    return {
        "status": "success",
        "reports": []
    }


@router.get("/reports/sales")
def sales_report():
    return {
        "status": "success",
        "report_type": "sales",
        "data": {
            "total_sales": 0,
            "total_orders": 0
        }
    }


@router.get("/reports/inventory")
def inventory_report():
    return {
        "status": "success",
        "report_type": "inventory",
        "data": {
            "total_products": 0,
            "low_stock_products": 0
        }
    }


@router.get("/reports/finance")
def finance_report():
    return {
        "status": "success",
        "report_type": "finance",
        "data": {
            "total_income": 0,
            "total_expense": 0,
            "profit": 0
        }
    }