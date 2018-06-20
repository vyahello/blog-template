import pytest
from datetime import datetime
from server.view.posts import PostDate, BlogPost, Date, Post

_fmt: str = '%B %d, %Y'


@pytest.fixture(scope="module")
def date() -> str:
    """Return current date time."""

    return datetime.strftime(datetime.today(), _fmt)


@pytest.fixture(scope="module")
def post_date() -> Date:
    """Return post date."""

    return PostDate()


@pytest.fixture(scope="module")
def blog_post() -> Post:
    """Return blog post."""

    return BlogPost()


@pytest.mark.unittest
def test_post_date(post_date: Date, date: str) -> None:
    assert post_date() == date


@pytest.mark.unittest
def test_blog_post(blog_post: Post, date: str) -> None:
    assert blog_post() == [
            {
                'author': 'Volodymyr Yahello',
                'title': 'Blog Post #1',
                'content': 'Test content',
                'date_posted': f"{date}"
            }
        ]
