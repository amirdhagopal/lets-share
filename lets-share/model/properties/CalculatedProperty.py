from google.appengine.ext import db

class CalculatedProperty(db.Property):

  def __init__(self, calc_fn, **kwds):
    """Constructor for CalculatedProperty.

    Args:
      calc_fn: a method to derive the property value.
               It can access any properties or other attributes
               of the data model to calculate the return value.
               The method, in order to compile properly, must be defined
               prior to the definition of this CalculatedProperty, 
               and any properties accessed by the method must be defined
               prior to the definition of the method.
               This makes it rather difficult to have circular references.
    """
    super(CalculatedProperty, self).__init__(**kwds)
    self.calc_fn = calc_fn

  def __get__(self, model_instance, model_class):
    """ Computes and returns the [calculated] value on the given model instance.

    See http://docs.python.org/ref/descriptors.html for a description of
    the arguments to this class and what they mean."""
    if model_instance is None:
      return self
    return self.derive_fn(model_instance)