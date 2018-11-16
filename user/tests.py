from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
from flask import session

from user.models import User

class UserTest(unittest.TestCase):
    def create_app(self):
        self.db_name = 'flaskbook_test'
        return create_app_base(
            MONGODB_SETTINGS={'DB': self.db_name},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY = 'mySecret',
            )

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)

    def user_dict(self):
        return dict(
        first_name="Marshal",
        last_name="Mori",
        username="marshal",
        email="marshal@marshal.com",
        password="123456",
        confirm="123456"
        )

    def test_register_user(self):
        # basic registration
        rv = self.app.post('/register', data=self.user_dict(), follow_redirects=True)
        assert User.objects.filter(username=self.user_dict()['username']).count() == 1

         # Invalid username characters
        user2 = self.user_dict()
        user2['username'] = "test test"
        user2['email'] = "test@example.com"
        rv = self.app.post('/register', data=user2, follow_redirects=True)
        assert 'Nome de usuário inválido.' in str(rv.data.decode('utf-8'))

        #Is username being saved in lowercase?
        user3 = self.user_dict()
        user2['username'] = "TestUser"
        user2['email'] = "test2@example.com"
        rv = self.app.post('/register', data=user3, follow_redirects=True)
        assert User.objects.filter(username=user3['username'].lower()).count() == 1

    def test_login_user(self):
        # create user
        self.app.post('/register', data=self.user_dict())
        # login user
        rv = self.app.post('/login', data=dict(
            username=self.user_dict()['username'],
            password=self.user_dict()['password']
            ))
        # check the session is set
        with self.app as c:
            rv = c.get('/')
            assert session.get('username') == self.user_dict()['username']

    def test_edit_profile(self):
        # create a user
        self.app.post('/register', data=self.user_dict())\
        # login the user
        rv = self.app.post('/login', data=dict(
            username=self.user_dict()['username'],
            password=self.user_dict()['password']
            ))
        # check that user has edit button on his own profile
        rv = self.app.get('/' + self.user_dict()['username'])
        assert "Editar" in str(rv.data)

        # edit fields
        user = self.user_dict()
        user['first_name'] = "Test First"
        user['last_name'] = "Test Last"
        user['username'] = "TestUsername"
        user['email'] = "Test@Example.com"

        # edit the user
        rv = self.app.post('/edit', data=user)
        assert "Profile atualizado." in str(rv.data)
        edited_user = User.objects.first()
        assert edited_user.first_name == "Test First"
        assert edited_user.last_name == "Test Last"
        assert edited_user.username == "testusername"
        assert edited_user.email == "test@example.com"

        # create a second user
        self.app.post('/register', data=self.user_dict())
        # login the user
        rv = self.app.post('/login', data=dict(
            username=self.user_dict()['username'],
            password=self.user_dict()['password']
            ))

        # try to save same email
        user = self.user_dict()
        user['email'] = "test@example.com"
        rv = self.app.post('/edit', data=user)
        assert "Esse email já foi cadastrado." in str(rv.data.decode('utf-8'))

        # try to save same username
        # user = self.user_dict()
        # user['username'] = "TestUsername"
        # rv = self.app.post('/edit', data=user)
        # print(str(rv.data))
        # assert "Nome de usuário já cadastrado." in str(rv.data.decode('utf-8'))
