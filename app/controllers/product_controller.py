from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.db_config import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import (
    DashboardSummary,
    MessageResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService


router = APIRouter(prefix="/api/products", tags=["Products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repository = ProductRepository(db)
    return ProductService(repository)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create_product(product_data)


@router.get("", response_model=list[ProductResponse])
def get_all_products(service: ProductService = Depends(get_product_service)):
    return service.get_all_products()


@router.get("/search", response_model=list[ProductResponse])
def search_products(
    name: str = Query(default="", min_length=0, description="Search by product name"),
    service: ProductService = Depends(get_product_service),
):
    return service.search_products(name)


@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(service: ProductService = Depends(get_product_service)):
    return service.get_dashboard_summary()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.get_product_by_id(product_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.update_product(product_id, product_data)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    try:
        service.delete_product(product_id)
        return {"message": "Product deleted successfully."}
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
