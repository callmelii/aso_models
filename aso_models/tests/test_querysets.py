from django.db import connection
from django.db.models.base import ModelBase
from django.test import TransactionTestCase
from django.utils import timezone

from ..models import AbstractShrewdModel
from ..querysets import ShrewdQuerySet


class ShrewdQuerySetTest(TransactionTestCase):

    abstract_model = AbstractShrewdModel

    @classmethod
    def setUpClass(cls):
        cls.model = ModelBase(
            f'__TestModel__{cls.abstract_model.__name__}',
            (cls.abstract_model,),
            {'__module__': cls.abstract_model.__module__}
        )
        super().setUpClass()

    def setUp(self):
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.model)

    def tearDown(self):
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.model)

    def test_mututally_exclusive_flags(self):
        '''
        Assert that a shrewd queryset cannot exist in its shrewd
        mode, and be operating on a recycle bin at the same time.
        '''
        with self.assertRaises(AssertionError) as cm:
            ShrewdQuerySet(self.model, on_recycle_bin=True)

        expected_error_msg = (
            'Shrewd queryset cannot exist in the shrewd mode and work on a '
            'recycle bin at the same time!'
        )
        self.assertEqual(str(cm.exception), expected_error_msg)