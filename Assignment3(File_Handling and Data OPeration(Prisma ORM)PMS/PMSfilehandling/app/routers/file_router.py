from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.models.product import Product
from app.schemas.product_schema import ProductCreate
from app.utils.file_utils import read_csv_to_dicts, export_to_csv

router = APIRouter(prefix="/file", tags=["File Handling"])

# 1️⃣ Upload CSV and insert into DB
@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = read_csv_to_dicts(file)
    for record in data:
        product = Product(**record)
        db.add(product)
    db.commit()
    return {"message": f"{len(data)} records inserted successfully!"}

# 2️⃣ Add single product via JSON
@router.post("/add")
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# 3️⃣ Download all or limited rows as CSV
@router.get("/download")
def download_data(
    db: Session = Depends(get_db),
    limit: int | None = Query(None)
):
    query = db.query(Product)
    if limit:
        query = query.limit(limit)
    products = query.all()

    data = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "company": p.company,
        }
        for p in products
    ]

    csv_stream = export_to_csv(data)
    return StreamingResponse(
        csv_stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"}
    )
