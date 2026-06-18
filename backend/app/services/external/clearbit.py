"""
Optional Clearbit integration, used to enrich a discovered competitor's
domain with a clean company name / description.

Requires CLEARBIT_API_KEY. If it isn't set, this module is skipped - the
similar-startup / competitor entries from other providers (or the knowledge
base) are used as-is, without enrichment.

Note: Clearbit's standalone API products have been folding into HubSpot's
"Breeze Intelligence" - check current availability/docs before relying on
this in production: https://clearbit.com/docs
"""
from typing import Optional

import httpx

from ...config import settings

ENRICH_URL = "https://company.clearbit.com/v2/companies/find"


def enrich_domain(domain: str) -> Optional[dict]:
    if not settings.CLEARBIT_API_KEY or not domain:
        return None

    try:
        with httpx.Client(timeout=settings.EXTERNAL_API_TIMEOUT_SECONDS) as client:
            resp = client.get(
                ENRICH_URL,
                params={"domain": domain},
                auth=(settings.CLEARBIT_API_KEY, ""),
            )
            if resp.status_code != 200:
                return None
            data = resp.json()

        return {
            "name": data.get("name"),
            "description": data.get("description"),
            "logo": data.get("logo"),
            "domain": domain,
        }
    except Exception:
        return None
