"""
Barcode generation logic using python-barcode and qrcode.
"""

import io
import base64
from typing import Optional

import barcode
from barcode.writer import SVGWriter, ImageWriter
import qrcode
from qrcode.image.svg import SvgPathImage
from qrcode.image.pil import PilImage


# Supported barcode formats mapped to python-barcode names
SUPPORTED_FORMATS = {
    "code39": "code39",
    "code128": "code128",
    "ean": "ean",
    "ean13": "ean13",
    "ean8": "ean8",
    "upca": "upca",
    "upce": "upce",
    "isbn10": "isbn10",
    "isbn13": "isbn13",
    "issn": "issn",
    "jan": "jan",
    "pzn": "pzn",
    "itf": "itf",
    "gs1-128": "gs1-128",
    "databar": "databar",
}


def validate_format(barcode_format: str) -> Optional[str]:
    """Validate and normalize the barcode format.

    Returns the normalized format name or None if unsupported.
    """
    fmt = barcode_format.lower().replace("-", "")
    # Map common aliases
    alias_map = {
        "code39": "code39",
        "code128": "code128",
        "ean": "ean13",
        "ean13": "ean13",
        "ean8": "ean8",
        "ean-13": "ean13",
        "ean-8": "ean8",
        "upc": "upca",
        "upca": "upca",
        "upc-a": "upca",
        "upce": "upce",
        "upc-e": "upce",
        "isbn": "isbn13",
        "isbn10": "isbn10",
        "isbn-10": "isbn10",
        "isbn13": "isbn13",
        "isbn-13": "isbn13",
        "issn": "issn",
        "jan": "jan",
        "pzn": "pzn",
        "itf": "itf",
        "gs1-128": "gs1-128",
        "databar": "databar",
        "code-39": "code39",
        "code-128": "code128",
    }
    return alias_map.get(fmt)


def generate_barcode_svg(barcode_format: str, data: str) -> str:
    """Generate a barcode as SVG string.

    Args:
        barcode_format: Normalized barcode format name.
        data: The data to encode.

    Returns:
        SVG string of the barcode.

    Raises:
        ValueError: If the format/data combination is invalid.
    """
    if barcode_format not in SUPPORTED_FORMATS:
        supported = sorted(SUPPORTED_FORMATS.keys())
        raise ValueError(
            f"Unsupported barcode format '{barcode_format}'. "
            f"Supported formats: {', '.join(supported)}"
        )

    writer = SVGWriter()
    barcode_class = barcode.get_barcode_class(barcode_format)
    code = barcode_class(data, writer=writer)
    return code.render().decode("utf-8")


def generate_barcode_png(barcode_format: str, data: str) -> bytes:
    """Generate a barcode as PNG bytes.

    Args:
        barcode_format: Normalized barcode format name.
        data: The data to encode.

    Returns:
        PNG bytes of the barcode.

    Raises:
        ValueError: If the format/data combination is invalid.
    """
    if barcode_format not in SUPPORTED_FORMATS:
        supported = sorted(SUPPORTED_FORMATS.keys())
        raise ValueError(
            f"Unsupported barcode format '{barcode_format}'. "
            f"Supported formats: {', '.join(supported)}"
        )

    writer = ImageWriter()
    barcode_class = barcode.get_barcode_class(barcode_format)
    code = barcode_class(data, writer=writer)
    buf = io.BytesIO()
    code.write(buf)
    return buf.getvalue()


def generate_qr_svg(data: str) -> str:
    """Generate a QR code as SVG string using path-based rendering.

    Args:
        data: The data to encode in the QR code.

    Returns:
        SVG string of the QR code.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    buf = io.BytesIO()
    qr.make_image(image_factory=SvgPathImage).save(buf)
    return buf.getvalue().decode("utf-8")


def generate_qr_png(data: str) -> bytes:
    """Generate a QR code as PNG bytes.

    Args:
        data: The data to encode in the QR code.

    Returns:
        PNG bytes of the QR code.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    buf = io.BytesIO()
    qr.make_image(image_factory=PilImage).save(buf, format="PNG")
    return buf.getvalue()
