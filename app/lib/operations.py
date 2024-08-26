import logging
from sqlalchemy import func
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models import Product as ModelProduct
from app.schemas import Family, Product, Sales


async def update_existing_product(db: Session, product_id: int, product: ModelProduct):
    _product_result = await db.execute(
        select(Product).filter(Product.product_id == product_id)
    )
    _product = _product_result.scalar()
    if _product:
        updated_data = product.model_dump(exclude_unset=True)
        for attr, value in updated_data.items():
            setattr(_product, attr, value)
        await db.commit()
        await db.refresh(_product)

        return _product
    else:
        raise HTTPException(
            status_code=404, detail=f"Product not found with id={product_id}"
        )


async def assign_family_to_product(db: Session, product_id: int, family_id: int):
    # product_results = await db.execute(select(Product).filter(Product.product_id == product_id)) # this is more practical
    product_result = await db.execute(select(Product).filter(Product.id == product_id))
    product = product_result.scalar()

    family_result = await db.execute(select(Family).filter(Family.id == family_id))
    family = family_result.scalar()

    logging.warning(f"Product: {product}, Family: {family}")
    if product and family:
        product.family = family
        await db.commit()
        return product
    else:
        raise HTTPException("Either product or family or both not found")


async def get_families(db: Session, product_id: int | None = None):
    if product_id:
        query = (
            select(Family).join(Family.product).filter(Product.product_id == product_id)
        )
    else:
        query = select(Family)

    result = await db.execute(query)
    return result.scalars().all()


async def get_products(product_id: int, family_id: int, db: Session):
    if product_id:
        query = select(Product).filter(Product.product_id == product_id)
    elif family_id:
        query = select(Product).join(Product.family).filter(Family.id == family_id)
    else:
        query = select(Product)

    result = await db.execute(query)

    return result.scalars().all()


async def get_sales(
    year_start: datetime,
    year_end: datetime,
    product_id: int,
    family_id: int,
    db: Session,
):
    if product_id:
        query = (
            select(func.sum(Sales.value))
            .join(Product)
            .filter(Product.product_id == product_id)
        )
    elif family_id:
        query = (
            select(func.sum(Sales.value))
            .join(Sales.product)
            .join(Product.family)
            .filter(Family.id == family_id)
        )
    else:
        query = select(func.sum(Sales.value))

    result = await db.execute(
        query.filter(Sales.date >= year_start, Sales.date < year_end)
    )

    return result.scalars().all() or 0


async def get_product_by_id(db: Session, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))

    return result.scalars().first()


async def get_family_by_name(db: Session, family_name: str):
    result = await db.execute(select(Family).where(Family.name == family_name))

    return result.scalars().first()


async def create_product(db: Session, product_data: dict):
    family = await get_family_by_name(db, product_data["Family"])
    if not family:
        family = Family(name=product_data["Family"])
        db.add(family)
        await db.commit()
        await db.refresh(family)

    product = Product(
        name=product_data["Product Name"],
        family_id=family.id,
        price=product_data["Price"],
        product_id=product_data["Product ID"],
    )
    db.add(product)

    await db.commit()
    await db.refresh(product)

    return product


async def update_sales(db: Session, product_id: int, sales_data: dict):
    for year_month, value in sales_data.items():
        year_month = datetime.strptime(year_month + "-01", "%Y-%m-%d")
        sales_record = await db.execute(
            select(Sales).where(
                Sales.product_id == product_id, Sales.date == year_month
            )
        )
        existing_sales = sales_record.scalars().first()
        if existing_sales:
            existing_sales.value = value
        else:
            new_sales = Sales(product_id=product_id, date=year_month, value=value)
            db.add(new_sales)
    await db.commit()
