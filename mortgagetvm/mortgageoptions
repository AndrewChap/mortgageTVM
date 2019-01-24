# Factory-like class for mortgage options
class MortgageOptions:
  def __init__(self,kind,**inputOptions):
    self.set_default_options()
    self.set_kind_options(kind = kind)
    self.set_input_options(**inputOptions)
    
  def set_default_options(self):
    self.optionList = dict()
    self.optionList['commonDefaults'] = dict(
      name                 =  None ,
      label                =  None , 
      houseCost            = '100%', # how much you are paying for the house
      mortgageRate         = '0.0%', # Mortgage annual interest rate
      mortgageLength       = '30Y' , # Mortgage length (in years)
      downPayment          = '0%'  , # Percentage of house cost paid upfront 
      startingCash         = '100%', # Amount of money you have before purchase
      tvmRate              = '7.0%', # Annual rate of return of savings
      inflationRate        = '1.8%', # Annual rate of inflation - NOT IMPLEMENTED
      appreciationRate     = '5.0%', # Annual rate of increase in value of house
      houseValue           = '100%', # how much the house is worth when you bought it
      originationFees      = '0.0%', # Mortgage fees as a percentage of the loan
      otherMortgageFees    = '0.0%', # Other fees as a percentage of the loan
      otherPurchaseFees    = '0.0%', # Other fees as a percentage of home value
      paymentsPerYear      = '12'  , # Number of mortgage payments per year
      taxRate              = '0.0%', # Annual taxes as percentage of home value
      insuranceRate        = '0.0%', # Annual insurance as percentage of home value
      listingFee           = '0.0%', # Cost of selling the house
      capitalGainsTax      = '0.0%', # Paid if selling house within two years
      capitalGainsPeriod   = '0'   , # Years after which cap gains tax is not applied
      rentalIncome         = '0.0%', # Monthly rental price as percentage of home value 
      rentalPayment        = '0.0%', # Monthly rental price as percentage of home value 
    )
    self.optionList['mortgageDefaults'] = dict(
      name                 = 'mortgage',
      label                = 'Mortgage',
      mortgageRate         = '4.5%', # Mortgage annual interest rate
      mortgageLength       = '30Y' , # Mortgage length (in years)
      downPayment          = '20%' , # Percentage of house cost paid upfront 
      startingCash         = '100%', # Amount of money you have before purchase
      originationFees      = '0.5%', # Mortgage fees as a percentage of the loan
      otherMortgageFees    = '0.5%', # Other fees as a percentage of the loan
      otherPurchaseFees    = '0.5%', # Other fees as a percentage of home value
      paymentsPerYear      = '12'  , # Number of mortgage payments per year
      taxRate              = '0.6%', # Annual taxes as percentage of home value
      insuranceRate        = '0.4%', # Annual insurance as percentage of home value
      listingFee           = '6.0%', # Cost of selling the house
      capitalGainsTax      = '15%' , # Paid if selling house within two years
      capitalGainsPeriod   = '2'   , # Years after which cap gains tax is not applied
    )
    self.optionList['rentalDefaults'] = dict(
      rentalPayment        = '0.6%', # Monthly rental price as percentage of home value
    )
    self.optionList['investmentPropertyDefaults'] = dict(
      mortgageRate         = '4.5%', # Mortgage annual interest rate
      mortgageLength       = '30Y' , # Mortgage length (in years)
      downPayment          = '20%' , # Percentage of house cost paid upfront 
      startingCash         = '100%', # Amount of money you have before purchase
      tvmRate              = '7.0%', # Annual rate of return of savings
      inflationRate        = '1.8%', # Annual rate of inflation - NOT IMPLEMENTED
      appreciationRate     = '5.0%', # Annual rate of increase in value of house
      houseValue           = '100%', # how much the house is worth when you bought it
      originationFees      = '0.5%', # Mortgage fees as a percentage of the loan
      otherMortgageFees    = '0.5%', # Other fees as a percentage of the loan
      otherPurchaseFees    = '0.5%', # Other fees as a percentage of home value
      paymentsPerYear      = '12'  , # Number of mortgage payments per year
      taxRate              = '0.6%', # Annual taxes as percentage of home value
      insuranceRate        = '0.4%', # Annual insurance as percentage of home value
      listingFee           = '6.0%', # Cost of selling the house
      capitalGainsTax      = '15%' , # Paid if selling house within two years
      capitalGainsPeriod   = '2'   , # Years after which cap gains tax is not applied
      rentalIncome         = '0.6%', # Monthly rental price as percentage of home value
    )

  def set_kind_options(self,kind,**inputOptions):
    self.options = self.optionList['commonDefaults']
    if kind == None:
      pass
    elif kind == 'mortgage':
      for key,val in self.optionList['mortgageDefaults'].items():
        self.options[key] = val
    elif kind == 'rental':
      for key,val in self.optionList['rentalDefaults'].items():
        self.options[key] = val
    elif kind == 'investmentProperty':
      for key,val in self.optionList['investmentPropertyDefaults'].items():
        self.options[key] = val

  def set_input_options(self,**inputOptions):
    for key,val in inputOptions.items():
      self.options[key] = val
