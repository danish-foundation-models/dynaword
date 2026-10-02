"""Create dummy news data with hand-set token counts and annotations."""

from pathlib import Path

from datasets import Dataset


TEXTS = [
    "Biblioteket åbner en ny læsesal på mandag.",
    "Byens svømmehal holder åbent hele sommeren.",
    "Et nyt tog forbinder de to byer fra december.",
]
ANNOTATIONS = {
    "content_integrity": "complete",
    "content_ratio": "complete_content",
    "content_length": "brief",
    "information_density": "adequate",
    "content_quality": "good",
    "educational_value": "minimal",
    "reasoning_indicators": "none",
    "content_safety": "safe",
    "pii_presence": "no_pii",
}


if __name__ == "__main__":
    source_dir = Path(__file__).parent
    documents = [
        {
            "id": f"news-{index}",
            "text": text,
            "source": "news",
            "added": "2026-01-01",
            "created": "2025-01-01, 2025-12-31",
            "token_count": token_count,
        }
        for index, (text, token_count) in enumerate(zip(TEXTS, [6, 9, 12]))
    ]
    metadata = [
        {"id": document["id"], "dataset": "news", **ANNOTATIONS}
        for document in documents
    ]
    Dataset.from_list(documents).to_parquet(source_dir / "data.parquet")
    Dataset.from_list(metadata).to_parquet(source_dir / "metadata.parquet")
