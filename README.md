# Barcode Generation API

A lightweight **barcode and QR code generation API** powered by FastAPI. Generate barcodes in Code128, Code39, EAN-13, UPC-A, ISBN, and more — plus QR codes — all from a single HTTP endpoint. Deploy on Railway in one click — no Dockerfile, no database, no external dependencies.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.com/new/template?templateUrl=https://github.com/INAPP-Mobile/railway-barcode-api)

## Features

- **13+ barcode formats** — Code128, Code39, EAN-13, EAN-8, UPC-A, UPC-E, ISBN-10, ISBN-13, ISSN, ITF, GS1-128, Databar, and QR codes
- **SVG or PNG output** — Use `?type=svg` or `?type=png` query parameter
- **No database needed** — Pure computation, zero persistent state
- **CORS enabled** — Ready for cross-origin requests from web apps
- **Memory-efficient** — Runs comfortably on Railway's free tier (512MB RAM)
- **Railpack auto-detect** — No Dockerfile needed
- **Tests included** — pytest suite for all endpoints

## API Reference

### GET `/barcode/{format}/{data}`

Generate a barcode or QR code.

| Parameter | Type | Description |
|-----------|------|-------------|
| `format` | path | Barcode symbology (see supported formats below) |
| `data` | path | Data to encode |
| `type` | query | Output format: `svg` (default) or `png` |

**Supported formats:**

`code128`, `code39`, `ean13`, `ean8`, `upca`, `upce`, `isbn10`, `isbn13`, `issn`, `itf`, `gs1-128`, `databar`, `qrcode`

**Examples:**

```bash
# QR code as SVG
curl https://your-app.railway.app/barcode/qrcode/hello-world

# Code128 as SVG
curl https://your-app.railway.app/barcode/code128/ABC-12345

# EAN-13 as SVG
curl https://your-app.railway.app/barcode/ean13/5901234123457

# QR code as PNG
curl https://your-app.railway.app/barcode/qrcode/hello-world?type=png
```

**Error responses (400):**

```json
{
  "detail": "Unsupported barcode format 'invalid'. Supported: code128, code39, ean13, ..."
}
```

### GET `/health`

Health check endpoint. Returns `{"status": "healthy", "version": "1.0.0"}`

### GET `/`

API root with version and link to docs.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Open API docs
open http://localhost:8000/docs
```

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.com/new/template?templateUrl=https://github.com/INAPP-Mobile/railway-barcode-api)

Click the button above, or follow these steps:
1. Fork/push this repo to your GitHub
2. Go to [Railway Dashboard](https://railway.com/dashboard) → New Project
3. Select **Deploy from GitHub repo**
4. Choose this repository
5. Railway auto-detects Python — no configuration needed
6. Click **Deploy**

## Environment Variables

This API has **no required environment variables**. Everything works out of the box.

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port (set automatically by Railway) | `8000` |

---

Published template for the Railway Template Kickback Program.
