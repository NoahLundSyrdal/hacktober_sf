# fuzzer/engine.py
import asyncio, random, time, json
import httpx
from typing import Dict, Any, Optional
from .store import save_finding

COMMON_PAYLOADS = [
    "", "null", "NaN", "∞", "🫠" * 2000,
    "' OR 1=1 --", "<script>alert(1)</script>",
    "../etc/passwd", '{"a":' + '1,' * 1000 + '0}',
    2**31, -1, 1e309
]

HEADERS = [
    {}, {"Accept": "application/xml"},
    {"X-Forwarded-For": "127.0.0.1"},
    {"Authorization": "Bearer badtoken"},
]

def mutate_value(value):
    # simple mutation strategy — extend in hackathon
    if random.random() < 0.4:
        return random.choice(COMMON_PAYLOADS)
    if isinstance(value, str):
        # insert long unicode or random chunk
        return value + random.choice(["", "🫠" * 50, "<script>alert(1)</script>"])
    if isinstance(value, int):
        return value * random.choice([0, -1, 2**12])
    return value

async def probe(client: httpx.AsyncClient, method: str, url: str, json_body: Optional[Dict[str,Any]]):
    t0 = time.perf_counter()
    try:
        r = await client.request(method, url, json=json_body, headers=random.choice(HEADERS), timeout=8.0)
        dt = int((time.perf_counter() - t0) * 1000)
        snippet = (r.text or "")[:500]
        return {"status": r.status_code, "ms": dt, "len": len(r.content), "snippet": snippet, "text": r.text}
    except Exception as e:
        return {"status": 0, "ms": None, "len": 0, "snippet": str(e)}

async def run_simple_scan(target_base: str, save_callback=save_finding, quick=True):
    """
    Simple route set; in production, crawl OpenAPI or spider endpoints.
    quick=True -> fewer mutations
    """
    routes = [
        ("POST", f"{target_base}/notes", {"title": "hello", "body": "world"}),
        ("GET",  f"{target_base}/notes/1", None),
        ("POST", f"{target_base}/upload", None),  # will use multipart below
        ("GET", f"{target_base}/admin/hidden", None),
    ]

    out = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for method, url, body in routes:
            # create several mutated attempts
            attempts = 3 if quick else 8
            for _ in range(attempts):
                if body:
                    mutated = {k: mutate_value(v) for k,v in body.items()}
                else:
                    mutated = None
                tasks.append(asyncio.create_task(probe(client, method, url, mutated)))
        results = await asyncio.gather(*tasks)
        # save suspicious results
        idx = 0
        for method, url, _ in routes:
            attempts = 3 if quick else 8
            for _ in range(attempts):
                res = results[idx]; idx += 1
                if res["status"] >= 500 or res["status"] == 0 or (res["ms"] is not None and res["ms"] > 1000):
                    payload = {"mutated": True}
                    # optional: attach request details for reproduction
                    save_callback(target_base, url, method, res["status"], res["ms"] or -1, res["snippet"], payload)
                out.append({"url": url, **res})
    return out
