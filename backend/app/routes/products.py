from fastapi import APIRouter

router = APIRouter()


@router.get("/products")
def get_products():
    return {
        "status": "success",
        "products": []
    }


@router.post("/products")
def add_product(product: dict):
    return {
        "status": "success",
        "message": "Product added successfully",
        "product": product
    }


@router.get("/products/{product_id}")
def get_product(product_id: str):
    return {
        "status": "success",
        "product_id": product_id
    }


@router.delete("/products/{product_id}")
def delete_product(product_id: str):
    return {
        "status": "success",
        "message": "Product deleted successfully",
        "product_id": product_id
    }