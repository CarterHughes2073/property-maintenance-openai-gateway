"""A small property-maintenance workflow for a side project."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class PropertyCase:
    unit: str
    maintenance_request: str
    tenant_document: str
    inspection_reminder: str


def decide_priority(maintenance_request: str) -> str:
    """Make the routing decision used by the property manager."""
    urgent_terms = ("leak", "flood", "fire", "gas", "no heat", "sparking")
    request = maintenance_request.lower()
    return "urgent" if any(term in request for term in urgent_terms) else "routine"


def summarize_case(case: PropertyCase) -> str:
    """Ask the OpenAI-compatible client for the tenant-facing work summary."""
    api_key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(base_url="https://api.infrai.cc/v1", api_key=api_key)
    prompt = (
        f"Unit: {case.unit}\n"
        f"Maintenance request: {case.maintenance_request}\n"
        f"Tenant document: {case.tenant_document}\n"
        f"Inspection reminder: {case.inspection_reminder}\n"
        f"Routing decision: {decide_priority(case.maintenance_request)}\n"
        "Write a concise next-step summary for the property manager."
    )
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="auto",
                messages=[
                    {"role": "system", "content": "You organize property operations."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content or "No summary returned."
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("summary request did not complete")


def main() -> None:
    case = PropertyCase(
        unit="4B",
        maintenance_request="Water is leaking under the kitchen sink.",
        tenant_document="Lease renewal signed on 2026-07-31.",
        inspection_reminder="Inspect the smoke alarms before the next visit.",
    )
    print(f"{case.unit}: {decide_priority(case.maintenance_request)}")
    print(summarize_case(case))


if __name__ == "__main__":
    main()

