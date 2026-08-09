from fastapi import APIRouter, HTTPException, status

from app.models.product import ProductCreate, ProductUpdate
from app.services.inventory_service import inventory_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def get_products():
    return {"success": True, "products": inventory_service.get_products()}


@router.post("", status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate):
    if inventory_service.find_product(product.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already exists. Edit it or add stock through voice.",
        )

    saved = inventory_service.add_product(
        name=product.name,
        quantity=product.quantity,
        category=product.category,
        purchase_price=product.purchasePrice,
        selling_price=product.sellingPrice,
        supplier=product.supplier,
        reorder_level=product.reorderLevel,
    )
    return {
        "success": True,
        "message": "Product added successfully",
        "product": saved,
    }


@router.get("/{product_id}")
def get_product(product_id: str):
    product = inventory_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "product": product}


@router.put("/{product_id}")
def update_product(product_id: str, product: ProductUpdate):
    payload = product.model_dump(exclude_none=True)
    saved = inventory_service.update_product(product_id, payload)
    if not saved:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "success": True,
        "message": "Product updated successfully",
        "product": saved,
    }


@router.delete("/{product_id}")
def delete_product(product_id: str):
    if not inventory_service.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "message": "Product deleted successfully"}
