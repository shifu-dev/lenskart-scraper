from abc import abstractmethod
import csv


class Writer:
    @abstractmethod
    def write_headers(self, headers: list[str]) -> None:
        return

    @abstractmethod
    def write_row(self, details: list) -> None:
        return


class ConsoleWriter(Writer):
    def write_headers(self, headers: list[str]) -> None:
        self.headers = headers

    def write_row(self, details: list) -> None:
        json = {}
        for header, value in zip(self.headers, details):
            json[header] = value

        print(json)

    headers: list[str]


class CsvWriter(Writer):

    def __init__(self, file: object) -> None:
        super().__init__()
        self._writer = csv.writer(file)

    def write_headers(self, headers: list[str]) -> None:
        self._writer.writerow(headers)

    def write_row(self, details: list) -> None:
        self._writer.writerow(details)

    _writer: object
