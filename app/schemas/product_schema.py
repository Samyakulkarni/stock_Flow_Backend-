from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=150)
    category: str = Field(..., min_length=1, max_length=100)
    selling_price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    description: str | None = Field(default="", max_length=2000)

    @field_validator("product_name", "category")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("This field cannot be empty.")
        return cleaned_value

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str:
        return value.strip() if value else ""


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardSummary(BaseModel):
    total_products: int
    total_quantity: int
    low_stock_products: int


class MessageResponse(BaseModel):
    message: str
