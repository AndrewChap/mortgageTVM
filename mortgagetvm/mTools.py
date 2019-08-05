from .mort import mort
import numpy as np

# Derived classes for mortgage attributes
# A mortgage attribute can be either a cost or a rate
# A cost can be defined as a percent, in which it needs
# to be multiplied by the given comparator

#TODO - treat cost % as a unit, but all rates should be unitless

class mCost(mort):
  def __init__(self, **kwargs):
    mort.__init__(self, **kwargs)
    if self.comparator is not None:
      if self.units == '%' or self.units is None:
        self.value *= self.comparator.value
        self.units  = self.comparator.units

class mRate(mort):
  def __init__(self, **kwargs):
    mort.__init__(self, **kwargs)
    # If the rate is given in a dollar amount, convert to percent
    # by dividing by comparator
    if self.units == '$':
      self.value = self.value/self.comparator.value
      self.units = '%'
        
    # TODO: look up proper names of cRate and fRate and change all the names accordingly
    # cRate is the rate divided by the number of times it
    # compounds in a year
    self.cRate = self.value/float(self.parent.paymentsPerYear.value)
    # fRate is the rate at which it would have to compound
    # per month in order reach the annual rate
    self.fRate = (1+self.value)**(1./self.parent.paymentsPerYear.value) - 1.0
    
class mTime(mort):
  def __init__(self, **kwargs):
    mort.__init__(self, **kwargs)
    
# A mortgage attribute can also be either a scalar
# or a vector, with time-dependent data

class mScalar:
  def __init__(self):
    self.data = None
    
class mVector:
  def __init__(self):
    # initialize all data points to initial value
    self.data = np.ones(self.parent.numDataPoints.value)*self.value

# Final Derived Classes
class mCostVector(mCost,mVector):
  def __init__(self, **kwargs):
    mCost.__init__(self, **kwargs)
    mVector.__init__(self)
  def inflationCorrect(self,monthlyInflationRate):
    for i,val in enumerate(self.data):
      inflationFactor = (1.0+monthlyInflationRate)**i
      self.data[i] /= inflationFactor

class mCostScalar(mCost,mScalar):
  def __init__(self, **kwargs):
    mCost.__init__(self, **kwargs)
    mScalar.__init__(self)

class mRateVector(mRate,mVector):
  def __init__(self, **kwargs):
    mRate.__init__(self, **kwargs)
    mVector.__init__(self)
    self.cData = self.data/self.parent.paymentsPerYear.value
    self.fData = self.fRate*np.ones(self.cData.size)
    
class mRateScalar(mRate,mScalar):
  def __init__(self, **kwargs):
    mRate.__init__(self, **kwargs)
    mScalar.__init__(self)
    
class mTimeScalar(mRate,mScalar):
  def __init__(self, **kwargs):
    mTime.__init__(self, **kwargs)
    mScalar.__init__(self)
    
class mTimeVector(mRate,mScalar):
  def __init__(self, **kwargs):
    mTime.__init__(self, **kwargs)
    #mVector.__init__(self)
    self.units = self.parent.mortgageLength.units
    self.data = np.linspace(0.0,
                            float(self.parent.mortgageLength.value),
                            self.parent.numDataPoints.value)
