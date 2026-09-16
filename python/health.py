import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def check_api_health(api_url: str, timeout: float = 5.0):
    url = f"{api_url.rstrip('/')}/health"

    request = Request(
        url,
        method="GET",
        headers={"Accept": "application/json"},
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")

            return {
                "status": "healthy",
                "http_status": response.status,
                "response": json.loads(body),
            }

    except HTTPError as exc:
        return {
            "status": "unhealthy",
            "http_status": exc.code,
            "error": f"API returned HTTP {exc.code}",
        }

    except URLError as exc:
        return {
            "status": "unhealthy",
            "http_status": None,
            "error": f"API connection failed: {exc.reason}",
        }

    except TimeoutError:
        return {
            "status": "unhealthy",
            "http_status": None,
            "error": "API request timed out",
        }