from django.forms import ValidationError
from django.test import TestCase
from .models import Thing
# Create your tests here.
class ThingModelTestCase(TestCase):
  
  def setUp(self):
    self.thing = Thing.objects.create(name = "something, that's a name", 
                                      description = "A description which should explain the thing but unfortunately it doesn't",
                                      quantity = 7)
  
  def test_name_is_not_blank(self):
    self.thing.name = ""
    self._assert_thing_is_invalid()
  
  def test_name_must_consist_of_30_characters_max(self):
    self.thing.name = "valid" * 7
    self._assert_thing_is_invalid()
  
  def test_name_is_unique(self):
    self.thing.name = "thing"
    Thing.objects.create(name = "thing", description = "doesn't matter", quantity = 15)
    self._assert_thing_is_invalid()
  
  def test_description_may_not_be_unique(self):
    self.thing.description = "Hello there!"
    Thing.objects.create(name = "a", description="Hello there!", quantity = 1)
    self._assert_thing_is_valid()
  
  def test_description_may_be_blank(self):
    self.thing.description = ""
    self._assert_thing_is_valid()
  
  def test_description_must_consist_of_120_characters_max(self):
    self.thing.description = "a" * 121
    self._assert_thing_is_invalid()
  
  def test_quantity_may_not_be_unique(self):
    self.thing.quantity = 12
    Thing.objects.create(name = "abc", description = "hi", quantity = 12)
    self._assert_thing_is_valid()
  
  def test_quantity_must_be_integer_less_than__or_equal_to_100(self):
    self.thing.quantity = 101
    self._assert_thing_is_invalid()
  
  def test_quantity_must_be_integer_more_than_or_equal_to_0(self):
    self.thing.quantity = -1
    self._assert_thing_is_invalid()
  
  def test_quantity_must_not_be_non_integer(self):
    self.thing.quantity = 1.4
    self._assert_thing_is_invalid()
    
  def _assert_thing_is_valid(self):
    try:
      self.thing.full_clean()
      
    except ValidationError:
      self.fail('Test thing should be valid')
      
  def _assert_thing_is_invalid(self):
    with self.assertRaises(ValidationError):
      self.thing.full_clean()