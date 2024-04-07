from abc import abstractmethod
from multiprocessing.pool import ThreadPool


class ScraperRunner:
    @abstractmethod
    def run(self, scraper: object, urls: list[str]) -> list[object]:
        pass


class SerialScraperRunner(ScraperRunner):
    def run(self, scraper: object, urls: list[str]) -> list[object]:
        results = []
        for url in urls:
            result = scraper.scrap(url)
            results.append(result)

        return results


class ParallelScraperRunner(ScraperRunner):
    def __init__(self, thread_count: int) -> None:
        self._pool = ThreadPool(thread_count)

    def __del__(self):
        self._pool.close()

    def run(self, scraper: object, urls: list[str]) -> list[object]:
        results = self._pool.map(lambda url: scraper.scrap(url), urls)
        return results

    _pool: ThreadPool
