"""
National Library of Medicine citation format
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

logger = get_logger(__name__)


class NLMJournalArticle(BaseCitationStyle):
    """
    Journal article formatting.
    """

    data: JournalArticleModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title. $journal_title. $year;$issue:$pages."
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


class NLMNewspaper(BaseCitationStyle):
    """
    Newspaper article formatting.
    """

    data: NewspaperModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title. $newspaper_title. $date.$year;$issue."
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


class NLMCitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников.
    """

    formatters_map = {
        JournalArticleModel.__name__: NLMJournalArticle,
        NewspaperModel.__name__: NLMNewspaper,
    }

    def __init__(self, models: list[BaseModel]) -> None:
        """
        Конструктор.

        :param models: Список объектов для форматирования
        """

        formatted_items = []
        for model in models:
            logger.info("model: " + str(model))
            logger.info("model type: " + str(type(model)))

            formatted_items.append(self.formatters_map.get(type(model).__name__)(model))  # type: ignore

        self.formatted_items = formatted_items

    def format(self) -> list[BaseCitationStyle]:
        """
        Форматирование списка источников.

        :return:
        """

        return sorted(self.formatted_items, key=lambda item: item.formatted)
