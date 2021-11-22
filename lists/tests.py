from django.test import TestCase


class SmokeTest(TestCase):
    ''' Smoke Test '''
    def test_bad_math(self):
        ''' Tets: Не правильные математические расчеты '''
        self.assertEqual(1 + 1, 3)
