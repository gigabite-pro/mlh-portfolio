import unittest
from peewee import *

from app import TimelinePost
from playhouse.shortcuts import model_to_dict

MODELS = [TimelinePost]

# Use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimeLinePost(unittest.TestCase):
    def setUp(self):
        # Bind model class to test db. Since we have a complete list of 
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessarry since SQLite in-memory database only live 
        # for the duration of connection, and in the next step, we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe', email='john@gmail.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@gmail.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2
        # TODO: Get timeline posts and assert that they are correct
        # Fetch timeline posts
        timeline_posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]

        # Check the details of the first post
        assert timeline_posts[1]['id'] == 1
        assert timeline_posts[1]['name'] == 'John Doe'
        assert timeline_posts[1]['email'] == 'john@gmail.com'
        assert timeline_posts[1]['content'] == 'Hello world, I\'m John!'

        # Check the details of the second post
        assert timeline_posts[0]['id'] == 2
        assert timeline_posts[0]['name'] == 'Jane Doe'
        assert timeline_posts[0]['email'] == 'jane@gmail.com'
        assert timeline_posts[0]['content'] == 'Hello world, I\'m Jane!'

