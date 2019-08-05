import re
import pandas as pd
# Base class for a mortgage attribute
# Handles either an inputString or an inputValue,
# finds units, then finds either inputValue or inputString
class mort:
  def __init__(self              ,
               parent            ,
               varName           ,
               label             ,
               inputString = None,
               value       = None,
               helpText    = None,
               units       = None,
               comparator  = None):

    self.parent      = parent  
    self.varName     = varName
    self.inputString = inputString
    self.label       = label
    self.value       = value
    self.helpText    = helpText
    self.units       = units
    self.comparator  = comparator
    
    self.plotThis    = False

    if varName in self.parent.options:
      self.inputString = self.parent.options[varName]
      
    if self.value is None and self.inputString is not None:
      self.value,self.units = self.str2val(s = self.inputString)
    
    if self.inputString is None:
      self.inputString = ''
      
  # class method for converting the input string into a value with units
  def str2val(self,s):
    # s - input string
    # f - units factor
    # u - units output
    # v - value output
    f = 1.0
    if '$' in s:
      u = '$'
    elif '%' in s:
      u = '%'
      f = 0.01
    elif 'Y' in s.upper():
      u = 'Y'
    elif 'M' in s.upper():
      u = 'M'
    else:
      u = None
    # remove any expected unit symbols as
    # well as spaces and commas from numbers
    numStr = re.sub("\$|%|Y|y|,| ", "", s)
    # convert remaining string to float
    try:
      v = f*float(numStr)
    except:
      raise
    return v,u
  
  # Override str method to just print the name
  def __str__(self):
    return self.varName
  
  # Method to add create a pandas series for adding to a DataFrame
  def makePandasRow(self,cols):
    dicts = {}
    for col in cols:
      attr = getattr(self,col)
      if attr is None:
        attr = ''
      dicts[col] = attr
    return pd.Series(dicts)
  
  # overridden in mCostVector
  def inflationCorrect(self,monthlyInflationRate):
    pass
