import pytz

from datetime import datetime
from unittest import mock

from django.db import connection
from django.db.models.base import ModelBase
from django.db.utils import OperationalError, ProgrammingError
from django.test import TestCase
from django.utils import timezone

from .models import AbstractTimeStamp


class AbstractModelMixinTest(TestCase):
    '''
    Base class for tests of model mixins / abstract models.
    To use, subclass and specify the mixin class variable.
    A model using the mixin will be available in self.model
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Create a dummy model which extends the mixin.
        A RunTimeWarning will occur if the model is registered twice.
        '''
        if not hasattr(cls, 'model'):
            cls.model = ModelBase(
                '__TestModel__' +
                cls.mixin.__name__, (cls.mixin,),
                {'__module__': cls.mixin.__module__}
            )

            # create a schema for our test model
            # if the table already exists, will pass
            try:
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(cls.model)
            except (OperationalError, ProgrammingError):
                pass
            super(AbstractModelMixinTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        '''
        Delete the schema for the test model. If no table, will pass
        '''
        super(AbstractModelMixinTest, cls).tearDownClass()
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(cls.model)
        except (OperationalError, ProgrammingError):
            pass


class AbstractTimeStampTest(AbstractModelMixinTest):
    """
    Test abstract timestamp model
    """
    mixin = AbstractTimeStamp

    def setUp(self):
        self.abstractTimeStampObj = self.model.objects.create()

    def test_created_at(self):
        mocked = datetime(2020, 4, 29, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            dummy_object = self.model.objects.create()
            self.assertEqual(dummy_object.created_at, mocked)

    def test_updated_at(self):
        mocked = timezone.now()
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            obj = self.abstractTimeStampObj
            obj.save()
            self.assertEqual(obj.updated_at, mocked)
