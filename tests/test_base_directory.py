import importlib
from pathlib import Path


def test_crawl4ai_base_directory_uses_fresh_nested_directory(tmp_path, monkeypatch):
    nested_base_dir = tmp_path / "fresh" / "nested"

    with monkeypatch.context() as context:
        context.setenv("CRAWL4_AI_BASE_DIRECTORY", str(nested_base_dir))

        async_database = importlib.import_module("crawl4ai.async_database")
        async_webcrawler = importlib.import_module("crawl4ai.async_webcrawler")

        async_database = importlib.reload(async_database)
        async_webcrawler = importlib.reload(async_webcrawler)

        crawler = async_webcrawler.AsyncWebCrawler(
            crawler_strategy=object(),
            verbose=False,
        )

        crawl4ai_dir = nested_base_dir / ".crawl4ai"

        assert crawl4ai_dir.is_dir()
        assert Path(async_database.base_directory) == crawl4ai_dir
        assert Path(async_database.DB_PATH) == crawl4ai_dir / "crawl4ai.db"
        assert Path(crawler.crawl4ai_folder) == crawl4ai_dir

    importlib.reload(async_database)
    importlib.reload(async_webcrawler)
