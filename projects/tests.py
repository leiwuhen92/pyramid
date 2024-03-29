import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'projects')

####################################################################################
    def test_hi(self):
        from .views import hi
        request = testing.DummyRequest()
        response = hi(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<body>Visit', response.body)

    def test_hello(self):
        from .views import hello
        request = testing.DummyRequest()
        response = hello(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Go back', response.body)

    def test_one(self):
        from .views import projectsviews
        request=testing.DummyRequest()
        response=projectsviews(request).one()
        self.assertEqual(response.status,'302 Found')

    def test_two(self):
        from .views import projectsviews
        request=testing.DummyRequest()
        response=projectsviews(request).two()
        self.assertEqual('two',response['name'])

    def test_plain_without_name(self):
        from .views import projectsviews
        request = testing.DummyRequest()
        response=projectsviews(request).plain()
        self.assertIn(b'No Name Provided', response.body)

    def test_plain_with_name(self):
        from .views import projectsviews
        request = testing.DummyRequest()
        request.GET['name']='wuhen'
        response=projectsviews(request).plain()
        self.assertIn(b'wuhen', response.body)


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from projects import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Pyramid' in res.body)

##############################################################################
    def test_hi(self):
        res = self.testapp.get('/hi', status=200)
        self.assertIn(b'<body>Visit', res.body) # “b” 将字符串转化为byte字节码，便于传输，用于网页请求响应

    def test_hello(self):
        res = self.testapp.get('/hello', status=200)
        self.assertIn(b'<body>Go back ', res.body) # “b” 将字符串转化为byte字节码，便于传输，用于网页请求响应

    def test_two(self):
        res = self.testapp.get('/two', status=200)
        self.assertIn(b'<h1>Hi two</h1>',res.body)

    def test_plain_without_name(self):
        res = self.testapp.get('/plain', status=200)
        self.assertIn(b'No Name Provided', res.body)

    def test_plain_with_name(self):
        res = self.testapp.get('/plain?name=wuhen', status=200)
        self.assertIn(b'wuhen', res.body)


    def test_css(self):
        res=self.testapp.get('/static/app.css',status=200)
        self.assertIn(b'body',res.body)

    def test_chapter14_json(self):
        res = self.testapp.get('/chapter14.json', status=200)
        self.assertIn(b'{"name": "two"}', res.body)
        self.assertEqual(res.content_type, 'application/json')



