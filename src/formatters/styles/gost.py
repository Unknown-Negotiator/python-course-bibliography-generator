"""
Стиль цитирования по ГОСТ Р 7.0.5-2008.
"""
from string import Template

from pydantic import BaseModel

from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    JournalArticleModel,
    NewspaperModel,
)
from formatters.styles.base import BaseCitationStyle
from logger import get_logger
from operator import itemgetter, attrgetter

logger = get_logger(__name__)

SORT_ORDER = {
    "GOSTBook": 0,
    "GOSTJournalArticle": 1,
    "GOSTCollectionArticle": 2,
    "GOSTNewspaper": 3,
    "GOSTInternetResource": 4,
}


class GOSTBook(BaseCitationStyle):
    """
    Форматирование для книг.
    """

    data: BookModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $title. – $edition$city: $publishing_house, $year. – $pages с."
        )

    def substitute(self) -> str:

        logger.info('Форматирование книги "%s" ...', self.data.title)

        return self.template.substitute(
            authors=self.data.authors,
            title=self.data.title,
            edition=self.get_edition(),
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )

    def get_edition(self) -> str:
        """
        Получение отформатированной информации об издательстве.

        :return: Информация об издательстве.
        """

        return f"{self.data.edition} изд. – " if self.data.edition else ""


class GOSTInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов.
    """

    data: InternetResourceModel

    @property
    def template(self) -> Template:
        return Template(
            "$article // $website URL: $link (дата обращения: $access_date)."
        )

    def substitute(self) -> str:

        logger.info('Форматирование интернет-ресурса "%s" ...', self.data.article)

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class GOSTCollectionArticle(BaseCitationStyle):
    """
    Форматирование для статьи из сборника.
    """

    data: ArticlesCollectionModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $collection_title. – $city: $publishing_house, $year. – С. $pages."
        )

    def substitute(self) -> str:

        logger.info('Форматирование сборника статей "%s" ...', self.data.article_title)

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            collection_title=self.data.collection_title,
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )


class GOSTJournalArticle(BaseCitationStyle):
    """
    Journal article formatting.
    """

    data: JournalArticleModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $journal_title. – $year. – № $issue. – С. $pages."
        )

    def substitute(self) -> str:
        logger.info('Journal article formatting "%s" ...', self.data.article_title)

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            journal_title=self.data.journal_title,
            year=self.data.year,
            issue=self.data.issue,
            pages=self.data.pages,
        )


class GOSTNewspaper(BaseCitationStyle):
    """
    Newspaper article formatting.
    """

    data: NewspaperModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $newspaper_title. – $year. – № $issue. – $date."
        )

    def substitute(self) -> str:
        logger.info('Newspaper article formatting "%s" ...', self.data.article_title)

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            newspaper_title=self.data.newspaper_title,
            year=self.data.year,
            date=self.data.date,
            issue=self.data.issue,
        )


class GOSTCitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников.
    """

    formatters_map = {
        BookModel.__name__: GOSTBook,
        InternetResourceModel.__name__: GOSTInternetResource,
        ArticlesCollectionModel.__name__: GOSTCollectionArticle,
        JournalArticleModel.__name__: GOSTJournalArticle,
        NewspaperModel.__name__: GOSTNewspaper,
    }

    def __init__(self, models: list[BaseModel]) -> None:
        """
        Конструктор.

        :param models: Список объектов для форматирования
        """

        formatted_items = []
        for model in models:
            formatted_items.append(self.formatters_map.get(type(model).__name__)(model))  # type: ignore

        self.formatted_items = formatted_items

    def format(self) -> list[BaseCitationStyle]:
        """
        Форматирование списка источников.

        :return:
        """
        return sorted(
            self.formatted_items,
            key=lambda item: (SORT_ORDER[type(item).__name__], item.formatted),
        )
