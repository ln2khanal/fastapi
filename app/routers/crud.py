from typing import Optional
from datetime import datetime
from app.models import Product
from app.lib.utils import get_db
from app.lib.operations import (
    get_families,
    get_products,
    get_sales,
    update_existing_product,
    assign_family_to_product,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/api/v1/crud")


@router.patch("/product/{product_id}", description="Updates a product")
async def update_product(
    product_id: int, product: Product, db: AsyncSession = Depends(get_db)
):
    _product = await update_existing_product(
        db=db, product_id=product_id, product=product
    )
    return {"product": _product}


@router.post("/family", description="Adds a product to a family")
async def assign_product_a_family(
    product_id: int, family_id: int, db: AsyncSession = Depends(get_db)
):
    product = await assign_family_to_product(
        db=db, product_id=product_id, family_id=family_id
    )

    return {"product": product}


@router.get(
    "/product",
    description="Lists the products. If no filters are supplied, all the table data is returned",
)
async def list_product(
    product_id: Optional[int] = Query(
        None,
        title="Product Id",
        description="Provide product category id to get the specific product details",
    ),
    family_id: Optional[int] = Query(
        None,
        title="Family Id",
        description="Provide family id to get the associated product details",
    ),
    db: AsyncSession = Depends(get_db),
):

    return {
        "data": await get_products(product_id=product_id, family_id=family_id, db=db)
    }


@router.get(
    "/family", description="Lists the product families. Supports family of a product"
)
async def list_product_family(
    product_id: Optional[int] = Query(
        None,
        title="Product Id",
        description="Provide product category id to get the family of the product",
    ),
    db: AsyncSession = Depends(get_db),
):
    return {"data": await get_families(product_id=product_id, db=db)}


@router.get(
    "/sales",
    description="Sums up the total sales for the given year ranges. Support product selection",
)
async def get_product_sales(
    product_id: Optional[int] = Query(
        None,
        title="Product Id",
        description="Provide product category id to get the sales of a specific product",
    ),
    family_id: Optional[int] = Query(
        None,
        title="Family Id",
        description="Provide family id to get the sales of a specific product family",
    ),
    year: Optional[int] = Query(
        None,
        title="Target Year",
        description="Provide year of which you want to get the sales",
        examples=[datetime.now().year],
    ),
    db: AsyncSession = Depends(get_db),
):
    if year is None:
        year = datetime.now().year

    year_start = datetime(year - 1, 1, 1)
    year_end = datetime(year, 1, 1)

    return {
        "data": await get_sales(
            year_start=year_start,
            year_end=year_end,
            product_id=product_id,
            family_id=family_id,
            db=db,
        ),
        "year_start": year_start,
        "year_end": year_end,
    }
