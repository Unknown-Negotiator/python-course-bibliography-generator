"""
Чтение исходного файла.
"""
from datetime import date
from typing import Type

import openpyxl
from openpyxl.workbook import Workbook

from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    JournalArticleModel,
    NewspaperModel,
)
from logger import get_logger
from readers.base import BaseReader

logger = get_logger(__name__)


class BookReader(BaseReader):
    """
    Чтение модели книги.
    """

    @property
    def model(self) -> Type[BookModel]:
        return BookModel

    @property
    def sheet(self) -> str:
        return "Книга"

    @property
    def attributes(self) -> dict:
        return {
            "authors": {0: str},
            "title": {1: str},
            "edition": {2: str},
            "city": {3: str},
            "publishing_house": {4: str},
            "year": {5: int},
            "pages": {6: int},
        }


class InternetResourceReader(BaseReader):
    """
    Чтение модели интернет-ресурса.
    """

    @property
    def model(self) -> Type[InternetResourceModel]:
        return InternetResourceModel

    @property
    def sheet(self) -> str:
        return "Интернет-ресурс"

    @property
    def attributes(self) -> dict:
        return {
            "article": {0: str},
            "website": {1: str},
            "link": {2: str},
            "access_date": {3: date},
        }


class ArticlesCollectionReader(BaseReader):
    """
    Чтение модели сборника статей.
    """

    @property
    def model(self) -> Type[ArticlesCollectionModel]:
        return ArticlesCollectionModel

    @property
    def sheet(self) -> str:
        return "Статья из сборника"

    @property
    def attributes(self) -> dict:
        return {
            "authors": {0: str},
            "article_title": {1: str},
            "collection_title": {2: str},
            "city": {3: str},
            "publishing_house": {4: str},
            "year": {5: int},
            "pages": {6: str},
        }


class JournalArticleReader(BaseReader):
    """
    Reading the journal article model.
    """

    @property
    def model(self) -> Type[JournalArticleModel]:
        return JournalArticleModel

    @property
    def sheet(self) -> str:
        return "Статья из журнала"

    @property
    def attributes(self) -> dict:
        return {
            "authors": {0: str},
            "article_title": {1: str},
            "journal_title": {2: str},
            "year": {3: int},
            "issue": {4: int},
            "pages": {5: str},
        }


class NewspaperReader(BaseReader):
    """
    Reading the newspaper article model.
    """

    @property
    def model(self) -> Type[NewspaperModel]:
        return NewspaperModel

    @property
    def sheet(self) -> str:
        return "Статья из газеты"

    @property
    def attributes(self) -> dict:
        return {
            "authors": {0: str},
            "article_title": {1: str},
            "newspaper_title": {2: str},
            "year": {3: int},
            "date": {4: str},
            "issue": {5: int},
        }


class SourcesReader:
    """
    Чтение из источника данных.
    """

    # зарегистрированные читатели
    gost_readers = [
        BookReader,
        InternetResourceReader,
        ArticlesCollectionReader,
        JournalArticleReader,
        NewspaperReader,
    ]

    nlm_readers = [JournalArticleReader, NewspaperReader]

    def __init__(self, path: str) -> None:
        """
        Конструктор.

        :param path: Путь к исходному файлу для чтения.
        """

        logger.info("Загрузка рабочей книги ...")
        self.workbook: Workbook = openpyxl.load_workbook(path)

    def read(self, citation_style: str = "gost") -> list:
        """
        Чтение исходного файла.

        :return: Список прочитанных моделей (строк).
        """

        items = []
        match citation_style:
            case "gost":
                readers = self.gost_readers
            case "nlm":
                readers = self.nlm_readers
        for reader in readers:
            logger.info("Чтение %s ...", reader)
            items.extend(reader(self.workbook).read())  # type: ignore

        return items
