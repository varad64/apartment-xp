import os
from typing import Optional
from fastapi import FastAPI, UploadFile, HTTPException, Form, File, status, Depends
from decimal import Decimal, ROUND_HALF_UP
from bill_extractor import parse_bill_gemma
from fastapi.middleware.cors import CORSMiddleware
from load_dotenv import load_dotenv

from model import Flat, ResolvedBill, FlatShare
from constants import create_flats

load_dotenv()

APARTMENT_NAME = os.getenv("APARTMENT_NAME")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

flats = create_flats()
total_area = sum(flat.total_chargeable_area for flat in flats)
print(f"Total area: {total_area}")

@app.get("/")
def home():
    return {f"Welcome, {APARTMENT_NAME} residents!"}

@app.get("/flats")
def get_flats() -> list[Flat]:
    return flats

@app.get("/flats/{flat_number}")
def get_flat_details(flat_number: int) -> Flat:
    return flats[flat_number]

@app.get("/total_area")
def get_total_area() -> int:
    return total_area

@app.post("/bills/batch-submit")
async def batch_submit_bills(
        security_amount: Optional[Decimal] = Form(None),
        security_image: Optional[UploadFile] = File(None),
        electricity_amount: Optional[Decimal] = Form(None),
        electricity_image: Optional[UploadFile] = File(None),
        water_amount: Optional[Decimal] = Form(None),
        water_image: Optional[UploadFile] = File(None),
):
    categories = [
        ("security", security_amount, security_image),
        ("common_electricity", electricity_amount, electricity_image),
        ("common_water", water_amount, water_image),
    ]

    resolved_items: list[ResolvedBill] = []

    for name, manual_val, file_obj in categories:
        if manual_val is not None and manual_val > Decimal("0.00"):
            resolved_items.append(ResolvedBill(category=name, amount=manual_val, source="manual_val"))
            continue

        if file_obj is not None and len(file_obj.filename) > 0:
            if file_obj.content_type not in ["image/jpeg", "image/jpg"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Uploaded file for {name} must be a JPEG image."
                )

            image_bytes = await file_obj.read()
            try:
                extracted_amount = await parse_bill_gemma(
                    image_bytes=image_bytes,
                    filename=file_obj.filename,
                    expected_category=name
                )
                resolved_items.append(
                    ResolvedBill(category=name, amount=extracted_amount, source="gemma_ocr")
                )
            except Exception as err:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Could not extract amount from {name} bll {str(err)}"
                )
            continue

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Missing input: Provide either an amount or an image for '{name}'"
        )

    total_to_split = sum(item.amount for item in resolved_items)
    flat_shares = compute_shares(total_to_split, total_area)

    return {
        "status": "success",
        "total_amount": total_to_split,
        "line_items": resolved_items,
        "shares": flat_shares,
    }

def compute_shares(total_amount: Decimal, total_area) -> list[FlatShare]:
    running_sum = Decimal("0.00")
    shares: list[FlatShare] = []

    for flat in flats:
        amount = ((total_amount/total_area) * flat.total_chargeable_area).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        shares.append(FlatShare(flat_number=flat.flat_number, area=flat.area, share_amount=amount))
        running_sum += amount

    discrepancy = total_amount - running_sum
    if discrepancy != Decimal("0.00"):
        largest = max(shares, key=lambda s: s.area)
        largest.share_amount += discrepancy

    return shares
