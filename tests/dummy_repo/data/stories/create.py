"""Create dummy stories with hand-set token counts and annotations."""

from pathlib import Path

from datasets import Dataset


TEXTS = [
    "En lille fugl sad i haven.",
    "Børnene fandt en gammel bog på loftet.",
    "Ved solnedgang sejlede båden hjem til øen.",
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
            "id": f"stories-{index}",
            "text": text,
            "source": "stories",
            "added": "2026-01-01",
            "created": "2025-01-01, 2025-12-31",
            "token_count": token_count,
        }
        for index, (text, token_count) in enumerate(zip(TEXTS, [6, 9, 12]))
    ]
    metadata = [
        {"id": document["id"], "dataset": "stories", **ANNOTATIONS}
        for document in documents
    ]
    Dataset.from_list(documents).to_parquet(source_dir / "data.parquet")
    Dataset.from_list(metadata).to_parquet(source_dir / "metadata.parquet")
