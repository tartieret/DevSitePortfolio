import json
import subprocess
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def build(out_dir: Path, settings: str = "pelicanconf.py", extra: list[str] | None = None) -> Path:
    cmd = [sys.executable, "-m", "pelican", "content", "-o", str(out_dir), "-s", settings]
    for item in extra or []:
        cmd += ["-e", item]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR" not in result.stdout + result.stderr, result.stdout + result.stderr
    return out_dir


@pytest.fixture(scope="session")
def site(tmp_path_factory) -> Path:
    return build(tmp_path_factory.mktemp("site"))


@pytest.fixture(scope="session")
def publish_site(tmp_path_factory) -> Path:
    return build(tmp_path_factory.mktemp("publish"), "publishconf.py")


@pytest.fixture(scope="session")
def paginated_site(tmp_path_factory) -> Path:
    return build(tmp_path_factory.mktemp("paginated"), extra=["DEFAULT_PAGINATION=2"])


def page(site_dir: Path, rel: str) -> BeautifulSoup:
    return BeautifulSoup((site_dir / rel).read_text(encoding="utf-8"), "html.parser")


def all_html(site_dir: Path) -> list[Path]:
    return sorted(site_dir.rglob("*.html"))


def json_ld(soup: BeautifulSoup) -> list[dict]:
    """Return every JSON-LD node on the page, flattening @graph."""
    nodes = []
    for script in soup.find_all("script", type="application/ld+json"):
        data = json.loads(script.string)
        nodes.extend(data.get("@graph", [data]))
    return nodes
