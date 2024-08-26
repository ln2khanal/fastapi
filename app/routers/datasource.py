import logging
import pandas as pd

from io import BytesIO
from app.lib.utils import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, Depends
from app.lib.operations import get_product_by_id, create_product, update_sales

xlsx_valid_pattern = b"PK\x03\x04"

router = APIRouter(prefix="/api/v1/datasource")


@router.post(
    "/add", description="Accepts .xlsx file and imports data into the database."
)
async def add_source(datafile: UploadFile = File(...), db: Session = Depends(get_db)):

    product_fields = {"Product Name", "Product ID", "Family", "Price"}

    file_content = await datafile.read()
    if not file_content.startswith(xlsx_valid_pattern):
        return JSONResponse(
            content={"error": "Please upload a valid .xlsx file."}, status_code=400
        )
    try:
        df = pd.read_excel(BytesIO(file_content), engine="openpyxl")
        sales_columns = set(df.columns.difference(product_fields))

        for index, row in df.iterrows():
            product = {p_f: row[p_f] for p_f in product_fields}
            sales = {s_f: row[s_f] for s_f in sales_columns}

            logging.debug(f"updating data; product={product}, sales={sales}")

            _product = await get_product_by_id(db, product["Product ID"])
            logging.debug(
                f"Existing product={_product}, product.id={product['Product ID']}"
            )

            if not _product:
                _product = await create_product(db, product)
                logging.debug(f"New product={_product} created")

            logging.debug(f"Updating sales")
            await update_sales(db, _product.id, sales)
        message = "File uploaded successfully"
    except Exception as e:
        logging.error(f"Couldn't process the file data, {e}")
        message = str(e)
    finally:
        return {"context": message}
