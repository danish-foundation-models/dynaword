"""Run the maintainer workflows against a small, disposable corpus."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib


def test_workflow(tmp_path: Path):
    repo = tmp_path / "dummy_repo"
    shutil.copytree(Path(__file__).parent / "dummy_repo", repo)
    env = os.environ.copy()
    env["DYNAWORD_REPO"] = str(repo)
    env["HF_HOME"] = str(tmp_path / "huggingface")
    env["HF_HUB_OFFLINE"] = "1"
    env["HF_DATASETS_OFFLINE"] = "1"
    env["MPLBACKEND"] = "Agg"
    env["PYTHONUTF8"] = "1"

    def run(*args):
        subprocess.run(
            [sys.executable, *args], cwd=repo, env=env, check=True, timeout=180
        )

    run("data/news/create.py")
    run("data/stories/create.py")
    run("-m", "dynaword.update_descriptive_statistics")

    # Two sources, each with three documents and synthetic token counts of 6, 9 and 12.
    stats = json.loads((repo / "descriptive_stats.json").read_text())
    assert stats["number_of_samples"] == 6
    assert stats["number_of_tokens"] == 54
    quality = stats["annotations"]["property_level_counts"]["content_quality"]
    assert quality["good"] == 6

    for source in ["news", "stories"]:
        stats_path = repo / "data" / source / "descriptive_stats.json"
        stats = json.loads(stats_path.read_text())
        assert stats["number_of_samples"] == 3
        assert stats["number_of_tokens"] == 27
        quality = stats["annotations"]["property_level_counts"]["content_quality"]
        assert quality["good"] == 3

    readme = (repo / "README.md").read_text()
    assert "**Number of samples**: 6" in readme
    assert "**Number of tokens (Llama 3)**: 54" in readme

    run("-m", "dynaword.bump_version")
    project = tomllib.loads((repo / "pyproject.toml").read_text())
    assert project["project"]["version"] == "0.1.1"
    assert "| **Version** | 0.1.1 " in (repo / "README.md").read_text()

    # Run the existing dataset checks against the generated dummy corpus.
    run("-m", "pytest", "--pyargs", "dynaword.tests", "--rootdir=.", "-q")
