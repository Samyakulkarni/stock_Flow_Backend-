from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_all(self) -> list[Product]:
        return (
            self.db.query(Product)
            .order_by(Product.created_date.desc(), Product.id.desc())
            .all()
        )

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update(self, product: Product, product_data: ProductUpdate) -> Product:
        for field, value in product_data.model_dump().items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def search_by_name(self, name: str) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(Product.product_name.ilike(f"%{name}%"))
            .order_by(Product.created_date.desc(), Product.id.desc())
            .all()
        )

    def get_dashboard_summary(self) -> dict[str, int]:
        total_products = self.db.query(func.count(Product.id)).scalar() or 0
        total_quantity = self.db.query(func.coalesce(func.sum(Product.quantity), 0)).scalar() or 0
        low_stock_products = (
            self.db.query(func.count(Product.id))
            .filter(Product.quantity <= 5)
            .scalar()
            or 0
        )

        return {
            "total_products": int(total_products),
            "total_quantity": int(total_quantity),
            "low_stock_products": int(low_stock_products),
        }
