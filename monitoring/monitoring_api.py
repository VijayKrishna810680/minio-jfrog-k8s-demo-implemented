from fastapi import APIRouter

router = APIRouter()

@router.get("/health/metrics")
def metrics():
    # Dummy Prometheus metrics endpoint
    return {
        "uptime_seconds": 123456,
        "requests_total": 7890,
        "errors_total": 12
    }

@router.get("/health/logs")
def logs():
    # Dummy logs endpoint
    return {
        "logs": [
            "2025-12-11T10:00:00Z INFO App started",
            "2025-12-11T10:01:00Z INFO User uploaded file report.pdf",
            "2025-12-11T10:02:00Z ERROR MinIO connection failed"
        ]
    }
