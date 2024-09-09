import pytest

from news.forms import CommentForm
from django.conf import settings


@pytest.mark.django_db
def test_news_count(object_list_home):
    """Проверка пагинации новостей."""
    news_count = object_list_home.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(object_list_home):
    """Проверка сортировки новостей."""
    all_dates = [news.date for news in object_list_home]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(response_detail):
    """Проверка сортировки комментариев."""
    assert 'news' in response_detail.context
    news = response_detail.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_parametrize, form_in_response',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False)
    )
)
def test_pages_contains_form(
    client_parametrize,
    form_in_response,
    detail_url
):
    """Проверка наличия формы в зависимости от авторизации."""
    response = client_parametrize.get(detail_url)
    assert ('form' in response.context) is form_in_response
    if form_in_response:
        assert isinstance(response.context['form'], CommentForm)
