from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(self, product_data: ProductCreate):
        return self.repository.create(product_data)

    def get_all_products(self):
        return self.repository.get_all()

    def get_product_by_id(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise LookupError("Product not found.")
        return product

    def update_product(self, product_id: int, product_data: ProductUpdate):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise LookupError("Product not found.")
        return self.repository.update(product, product_data)

    def delete_product(self, product_id: int) -> None:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise LookupError("Product not found.")
        self.repository.delete(product)

    def search_products(self, name: str):
        cleaned_name = name.strip()
        if not cleaned_name:
            return self.repository.get_all()
        return self.repository.search_by_name(cleaned_name)

    def get_dashboard_summary(self):
        return self.repository.get_dashboard_summary()
