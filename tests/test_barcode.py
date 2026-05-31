import pytest

from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["app"] == "Barcode Generation API"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_qr_code_svg(client):
    resp = await client.get("/barcode/qrcode/hello-world")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
    body = resp.text
    assert "<svg" in body
    assert "xmlns" in body


@pytest.mark.asyncio
async def test_qr_code_png(client):
    resp = await client.get("/barcode/qrcode/hello-world?type=png")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert len(resp.content) > 100


@pytest.mark.asyncio
async def test_code128_svg(client):
    resp = await client.get("/barcode/code128/ABC-12345")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
    assert "<svg" in resp.text


@pytest.mark.asyncio
async def test_code128_png(client):
    resp = await client.get("/barcode/code128/ABC-12345?type=png")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert len(resp.content) > 100


@pytest.mark.asyncio
async def test_ean13_svg(client):
    resp = await client.get("/barcode/ean13/5901234123457")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
    assert "<svg" in resp.text


@pytest.mark.asyncio
async def test_code39_svg(client):
    resp = await client.get("/barcode/code39/HELLO-WORLD")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
    assert "<svg" in resp.text


@pytest.mark.asyncio
async def test_invalid_format_returns_400(client):
    resp = await client.get("/barcode/invalid-format/some-data")
    assert resp.status_code == 400
    data = resp.json()
    assert "detail" in data
    assert "Unsupported" in data["detail"]


@pytest.mark.asyncio
async def test_empty_data_returns_400(client):
    resp = await client.get("/barcode/code128/%20")
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_invalid_output_type_returns_400(client):
    resp = await client.get("/barcode/code128/test?type=pdf")
    assert resp.status_code == 400
    assert "Unsupported output type" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_upca_svg(client):
    resp = await client.get("/barcode/upca/123456789012")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
    assert "<svg" in resp.text


@pytest.mark.asyncio
async def test_isbn13_svg(client):
    resp = await client.get("/barcode/isbn13/9781234567897")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
    assert "<svg" in resp.text


@pytest.mark.asyncio
async def test_long_data_in_qr(client):
    """QR codes can handle long data (up to ~3KB)."""
    long_data = "a" * 500
    resp = await client.get(f"/barcode/qrcode/{long_data}")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
