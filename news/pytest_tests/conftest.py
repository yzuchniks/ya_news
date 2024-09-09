from datetime import datetime, timedelta
from django.utils import timezone

import pytest
from django.test.client import Client

from news.models import Comment, News
from django.conf import settings
from django.urls import reverse


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Текст заметки',
        author=author,
    )
    return comment


@pytest.fixture
def id_for_news(news):
    return (news.id,)


@pytest.fixture
def id_for_comment(comment):
    return (comment.id,)


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(id_for_news):
    return reverse('news:detail', args=id_for_news)


@pytest.fixture
def object_list_home(client, home_url):
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    response = client.get(home_url)
    return response.context['object_list']


@pytest.fixture
def response_detail(author, news, author_client, detail_url):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return author_client.get(detail_url)


@pytest.fixture
def form_data():
    return {'text': 'Новый текст'}


@pytest.fixture
def edit_url(id_for_comment):
    return reverse('news:edit', args=id_for_comment)


@pytest.fixture
def delete_url(id_for_comment):
    return reverse('news:delete', args=id_for_comment)
