"""
Описание схем объектов (DTO).
"""

from typing import Optional

from pydantic import BaseModel, Field


class BookModel(BaseModel):
    """
    Модель книги:

    .. code-block::

        BookModel(
            authors="Иванов И.М., Петров С.Н.",
            title="Наука как искусство",
            edition="3-е",
            city="СПб.",
            publishing_house="Просвещение",
            year=2020,
            pages=999,
        )
    """

    authors: str
    title: str
    edition: Optional[str]
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: int = Field(..., gt=0)

    @property
    def trim_authors_dots(self):
        self.authors = self.authors.rstrip(".")


class InternetResourceModel(BaseModel):
    """
    Модель интернет ресурса:

    .. code-block::

        InternetResourceModel(
            article="Наука как искусство",
            website="Ведомости",
            link="https://www.vedomosti.ru/",
            access_date="01.01.2021",
        )
    """

    article: str
    website: str
    link: str
    access_date: str


class ArticlesCollectionModel(BaseModel):

    """
    Модель сборника статей:

    .. code-block::

        ArticlesCollectionModel(
            authors="Иванов И.М., Петров С.Н.",
            article_title="Наука как искусство",
            collection_title="Сборник научных трудов",
            city="СПб.",
            publishing_house="АСТ",
            year=2020,
            pages="25-30",
        )
    """

    authors: str
    article_title: str
    collection_title: str
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: str


class JournalArticleModel(BaseModel):

    """
    Модель статьи из журнала:

    .. code-block::

        JournalArticleModel(
            authors="Richard Evans, Alexander Pritzel, Tim Green.",
            article_title="Highly accurate protein structure prediction with AlphaFold",
            journal_title="Nature",
            year=2021,
            issue=596,
            pages="583-589"
        )
    """

    authors: str
    article_title: str
    journal_title: str
    year: int = Field(..., gt=0)
    issue: int = Field(..., gt=0)
    pages: str


class NewspaperModel(BaseModel):

    """
    Модель статьи из газеты:

    .. code-block::

        NewspaperModel(
            authors="Austen Hufford.",
            article_title="Some $191 Billion in Pandemic Payments May Have Been Improper, Labor Inspector General Says",
            newspaper_title="The Wall Street Journal",
            year=2023,
            date="08.02",
            issue=10
        )
    """

    authors: str
    article_title: str
    newspaper_title: str
    year: int = Field(..., gt=0)
    date: str
    issue: int = Field(..., gt=0)
