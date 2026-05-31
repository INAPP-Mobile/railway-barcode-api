"""
FastAPI app for barcode generation.

Exposes:
  GET /health           — Health check
  GET /                 — API info
  GET /barcode/{format}/{data} — Generate barcode/QR code
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

import barcode

from app.barcode_gen import (
    validate_format,
    generate_barcode_svg,
    generate_barcode_png,
    generate_qr_svg,
    generate_qr_png,
)

app = FastAPI(
    title="Barcode Generation API",
    version="1.0.0",
    description="Generate barcodes and QR codes in SVG or PNG format. "
    "Supports Code128, Code39, EAN-13, EAN-8, UPC-A, UPC-E, ISBN, ISSN, QR, and more.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "app": "Barcode Generation API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "/barcode/{format}/{data}": "Generate barcode (format=qrcode, code128, ean13, etc.)",
        },
    }


@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/barcode/{barcode_format:str}/{data:str}")
def generate_barcode(
    barcode_format: str,
    data: str,
    format_type: str = Query(
        "svg", alias="type", description="Output format: 'svg' or 'png'"
    ),
):
    """Generate a barcode or QR code.

    Args:
        barcode_format: Barcode symbology (code128, ean13, qrcode, code39, upca, etc.).
        data: Data to encode in the barcode.
        format_type: Output format — 'svg' (default) or 'png'.

    Returns:
        SVG or PNG image of the barcode.

    Raises:
        400: If the format is invalid or data can't be encoded.
    """
    if not data.strip():
        raise HTTPException(status_code=400, detail="Data cannot be empty")

    if format_type not in ("svg", "png"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported output type '{format_type}'. Use 'svg' or 'png'.",
        )

    # Handle QR code separately
    fmt_lower = barcode_format.lower()
    if fmt_lower == "qrcode" or fmt_lower == "qr":
        try:
            if format_type == "svg":
                svg_content = generate_qr_svg(data)
                return Response(content=svg_content, media_type="image/svg+xml")
            else:
                png_bytes = generate_qr_png(data)
                return Response(content=png_bytes, media_type="image/png")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to generate QR code: {str(e)}",
            )

    # Normalize barcode format
    normalized = validate_format(barcode_format)
    if normalized is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported barcode format '{barcode_format}'. "
            f"Supported: code128, code39, ean13, ean8, upca, upce, "
            f"isbn10, isbn13, issn, itf, gs1-128, databar, and qrcode",
        )

    # Generate the barcode
    try:
        if format_type == "svg":
            svg_content = generate_barcode_svg(normalized, data)
            return Response(content=svg_content, media_type="image/svg+xml")
        else:
            png_bytes = generate_barcode_png(normalized, data)
            return Response(content=png_bytes, media_type="image/png")
    except barcode.errors.IllegalCharacterError:
        raise HTTPException(
            status_code=400,
            detail=f"Data contains characters not supported by '{barcode_format}' format",
        )
    except barcode.errors.NumberOfDigitsError:
        raise HTTPException(
            status_code=400,
            detail=f"Data length is incorrect for '{barcode_format}' format. "
            f"EAN-13 requires 12 digits, EAN-8 requires 7 digits, UPC-A requires 11 digits.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate barcode: {str(e)}",
        )
