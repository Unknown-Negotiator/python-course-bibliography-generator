"""
Фикстуры для моделей объектов (типов источников).
"""
import pytest

from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    JournalArticleModel,
    NewspaperModel,
)


@pytest.fixture
def book_model_fixture() -> BookModel:
    """
    Фикстура модели книги.

    :return: BookModel
    """

    return BookModel(
        authors="Иванов И.М., Петров С.Н.",
        title="Наука как искусство",
        edition="3-е",
        city="СПб.",
        publishing_house="Просвещение",
        year=2020,
        pages=999,
    )


@pytest.fixture
def internet_resource_model_fixture() -> InternetResourceModel:
    """
    Фикстура модели интернет-ресурса.

    :return: InternetResourceModel
    """

    return InternetResourceModel(
        article="Наука как искусство",
        website="Ведомости",
        link="https://www.vedomosti.ru",
        access_date="01.01.2021",
    )


@pytest.fixture
def articles_collection_model_fixture() -> ArticlesCollectionModel:
    """
    Фикстура модели сборника статей.

    :return: ArticlesCollectionModel
    """

    return ArticlesCollectionModel(
        authors="Иванов И.М., Петров С.Н.",
        article_title="Наука как искусство",
        collection_title="Сборник научных трудов",
        city="СПб.",
        publishing_house="АСТ",
        year=2020,
        pages="25-30",
    )


@pytest.fixture
def journal_article_model_fixture() -> JournalArticleModel:
    """
    Фикстура модели сборника статей.

    :return: JournalArticleModel
    """

    return JournalArticleModel(
        authors="Richard Evans, Alexander Pritzel, Tim Green.",
        article_title="Highly accurate protein structure prediction with AlphaFold",
        journal_title="Nature",
        year=2021,
        issue=596,
        pages="583-589",
    )


@pytest.fixture
def newspaper_model_fixture() -> NewspaperModel:
    """
    Фикстура модели сборника статей.

    :return: JournalArticleModel
    """

    return NewspaperModel(
        authors="Austen Hufford.",
        article_title="Some $191 Billion in Pandemic Payments May Have Been Improper, Labor Inspector General Says",
        newspaper_title="The Wall Street Journal",
        year=2023,
        issue=10,
        date="08.02",
    )
