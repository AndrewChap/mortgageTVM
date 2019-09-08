from .mortgageBase import MortgageBase
from .mTools import *
import pandas as pd
import pdb
db = pdb.set_trace
# Main class for an individual mortgage
# Made for use with the MortgageComparison class,
# which compares multiple mortgages
class Mortgage(MortgageBase):
  
  # TODO: Add:
  #            - Add in maintenance costs
  #            - Scaling down due to inflation
  #            - Boolean for whether owner will be living in home
  # Long term TODO:
  #            - Allow rates like tvm, inflation, appreciation, to fluctuate
  #              Use either historical data or a distribution function to 
  #              create probability distribution function outputs

  # Initialization function with default values
  def __init__(self, kind = None, **options):
    if kind == None:
      kind = 'mortgage'
    self.options = self.populateOptions(kind,**options)  # set default attributes
    self.setAttributes(self.options)
    self.calculateMonthlyPayment()

  def setAttributes(self,options):  
    self.updateAttributes(options)  
    if options['name'] is None:
      self.name = 'myMortgage'
    else:
      self.name = options['name']
    self.customName = self.name  
    if options['label'] is None:
      self.label = self.name
    else:
      self.label = options['label']
    self.color = options['color']  

  def updateAttributes(self,options):
  
    # self.fieldlist must be initialized to an empty list before 
    # calling self.addAttribute()
    self.fieldList = []
    
    # Choose columns for when displaying mortgage attribute DataFrame
    self.df = pd.DataFrame(columns=['label',
                                    'inputString',
                                    'value',
                                    'units',
                                    'comparator',
                                    'helpText'])
  
    # Add input attributes to mortgage
    self.addAttribute(mCostScalar(parent      = self,
                                  varName     = 'houseCost',
                                  label       = 'House Cost',
                                  helpText    = 'Purchase price of '
                                                'the house'))
    self.addAttribute(mTimeScalar(parent      = self,
                                  varName     = 'mortgageLength',
                                  label       = 'Mortgage Length',
                                  helpText    = 'The loan term of '
                                                'the mortgage'))
    # TODO: maybe we shouldn't be using the base class for these next 
    # few?  Perhaps should make a unitless scalar/vector class
    self.addAttribute(mort       (parent      = self,
                                  varName     = 'paymentsPerYear',
                                  label       = 'payments/year',
                                  helpText    = 'Number of mortgage payments '
                                                'made per year'))
    self.addAttribute(mort       (parent      = self,
                                  value       = int(self.paymentsPerYear.value* \
                                                    self.mortgageLength.value),
                                  varName     = 'numPayments',
                                  label       = 'Number of payments',
                                  helpText    = 'Total number of mortgage '
                                                'payments'))
    self.addAttribute(mort       (parent      = self,
                                  value       = self.numPayments.value+1,
                                  varName     = 'numDataPoints',
                                  label       = 'Number of data points',
                                  helpText    = 'Number of data points for '
                                                'plotting'))
    self.addAttribute(mRateVector(parent      = self,
                                  varName     = 'mortgageRate',
                                  label       = 'Mortgage Rate',
                                  helpText    = 'Annual interest rate '
                                                'of the mortgage'))
    self.addAttribute(mCostScalar(parent      = self,
                                  varName     = 'downPayment',
                                  label       = 'Down Payment',
                                  comparator  = self.houseCost,
                                  helpText    = 'Mortgage down payment'))
    # TODO: Change "loanSize" to "loanAmount"
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.houseCost.value - \
                                                self.downPayment.value,
                                  varName     = 'loanSize',
                                  label       = 'Loan Size',
                                  units       = self.houseCost.units,
                                  helpText    = 'Size of the loan'))
    self.addAttribute(mCostScalar(parent      = self,
                                  varName     = 'startingCash',
                                  label       = 'Starting Cash',
                                  comparator  = self.houseCost,
                                  helpText    = 'Amount of cash on hand '
                                                'prior to home purchase'))
    self.addAttribute(mRateVector(parent      = self,
                                  varName     = 'tvmRate',
                                  label       = 'TVM rate',
                                  helpText    = 'Time-value rate of money '
                                                'i.e. the annual return on '
                                                'investment of savings, if '
                                                'invested in stock market'))
    self.addAttribute(mRateVector(parent      = self,
                                  varName     = 'inflationRate',
                                  label       = 'Inflation Rate',
                                  helpText    = 'Rate of inflation '
                                                'year-over-year'))
    self.addAttribute(mRateVector(parent      = self,
                                  varName     = 'appreciationRate',
                                  label       = 'Appreciation Rate',
                                  helpText    = 'Annual rate of appreciation '
                                                'on the home''s value'))
    self.addAttribute(mCostVector(parent      = self,
                                  varName     = 'houseValue',
                                  label       = 'House Value',
                                  comparator  = self.houseCost,
                                  helpText    = 'The resale value of the '
                                                'home'))
    self.addAttribute(mCostScalar(parent      = self,
                                  varName     = 'originationFees',
                                  label       = 'Origination Fees',
                                  comparator  = self.loanSize,
                                  helpText    = 'Amount of fees paid upfront '
                                                'for the mortgage'))
    self.addAttribute(mCostScalar(parent      = self,
                                  varName     = 'otherMortgageFees',
                                  label       = 'Other mortgage fees',
                                  comparator  = self.loanSize,
                                  helpText    = 'Other mortgage fees paid '
                                                'upfront'))
    self.addAttribute(mCostScalar(parent      = self,
                                  varName     = 'otherPurchaseFees',
                                  label       = 'Other purchase fees',
                                  comparator  = self.houseCost,
                                  helpText    = 'Other purchase fees paid '
                                                'upfront'))
    self.addAttribute(mRateVector(parent      = self,
                                  varName     = 'taxRate',
                                  label       = 'Tax Rate',
                                  helpText    = 'Property tax, as a portion of '
                                                'home value'))
    self.addAttribute(mRateVector(parent      = self,
                                  varName     = 'insuranceRate',
                                  label       = 'Insurance Rate',
                                  helpText    = 'Insurance cost, as a portion of '
                                                'home value'))
    self.addAttribute(mRateScalar(parent      = self,
                                  varName     = 'listingFee',
                                  label       = 'Listing Fee',
                                  comparator  = self.houseValue,
                                  helpText    = 'Fee paid if you sell your '
                                                'house'))
    self.addAttribute(mRateScalar(parent      = self,
                                  varName     = 'capitalGainsTax',
                                  label       = 'Cap. Gains Tax',
                                  comparator  = self.houseValue,
                                  helpText    = 'Tax paid if you sell your '
                                                'house within two years of '
                                                'purhcase, or if house is being '
                                                'used as a rental property'))
    self.addAttribute(mort       (parent      = self,
                                  varName     = 'capitalGainsPeriod',
                                  label       = 'Cap. Gains Period',
                                  helpText    = 'Number of years after which '
                                                'if you sell the house you wont '
                                                'pay capital gains tax'))
    self.addAttribute(mRateVector(parent      = self,
                                  varName     = 'rentalIncome',
                                  label       = 'Rental income',
                                  comparator  = self.houseValue,
                                  helpText    = 'Rental income, as a portion of '
                                                'home value'))
    
    self.addAttribute(mCostVector(parent      = self,
                                  varName     = 'rentalPayment',
                                  label       = 'Rental payment',
                                  comparator  = self.houseValue,
                                  helpText    = 'Rental payment, as a portion of '
                                                'home value'))
    # Call method to calculate monthly payment (principal + interest only)

      
  def addAttribute(self,attribute):
    # TODO: check for duplicate attributes and find and overwrite
    # field if it exists
    self.fieldList.append(attribute)
    setattr(self,attribute.varName,attribute)
    self.df.loc[attribute.varName] = attribute.makePandasRow(self.df.columns)
    
  def printAttributes(self):
    for field in self.fieldList:
      print("{}   {}   {}   {}   {}   {}".format(field.label      ,
                                                 field.inputString,
                                                 field.value      ,
                                                 field.units      ,
                                                 field.comparator ,
                                                 field.helpText   ,))
  
  def printDataframe(self):
    display(self.df)

  def calculateMonthlyPayment(self):
    l = self.loanSize.value
    c = self.mortgageRate.cRate
    n = self.numPayments.value
    
    # TODO: only catch if divide by zero
    try:
      monthlyPayment = l*(c*(1+c)**n)/((1+c)**n - 1)
    except:
      monthlyPayment = 0
        
    self.addAttribute(mCostVector(parent      = self,
                                  value       = monthlyPayment,
                                  varName     = 'monthlyPayment',
                                  label       = 'Monthly Payment',
                                  helpText    = 'Monthly payment (principal '
                                                '+ interest)'))

  def update_mortgage(self,options):
      for key,val in options.items():
          self.options[key] = val
      self.updateAttributes(self.options)
      self.calculateMonthlyPayment()

  def simulateMortgage(self):
    self.addAttribute(mTimeVector(parent      = self,
                                  varName     = 'timeVector',
                                  label       = 'Time',
                                  helpText    = 'Vector with data points for '
                                                'each mortgage payment, with '
                                                'the zeroth point representing '
                                                'the values before the '
                                                'mortgage'))
    # Make some new cost-vector attributes for calculating

    self.addAttribute(mCostScalar(parent      = self,
                                  value       = self.originationFees.value   + \
                                                self.otherMortgageFees.value + \
                                                self.otherPurchaseFees.value,
                                  varName     = 'allPurchaseFees',
                                  label       = 'All Purchase Fees',
                                  helpText    = 'Total fees when purchasing'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.startingCash.value      - \
                                                self.downPayment.value       - \
                                                self.allPurchaseFees.value,
                                  varName     = 'savings',
                                  label       = 'Savings',
                                  helpText    = 'Total amount of savings that '
                                                'compounds at the TVM rate'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'interestPayment',
                                  label       = 'Interest Payment',
                                  helpText    = 'Portion of mortgage payments '
                                                'that pay down interest'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'principalPayment',
                                  label       = 'Principal Payment',
                                  helpText    = 'Portion of mortgage payments '
                                                'that pay down principal'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'tPlusI',
                                  label       = 'Cum. Tax + Insurance',
                                  helpText    = 'Total cumulative payments '
                                                'to taxes and insurance'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'interest',
                                  label       = 'Interest payment',
                                  helpText    = 'Monthly payement to '
                                                'interest'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'principal',
                                  label       = 'Principal payment',
                                  helpText    = 'Monthly payement to '
                                                'principal'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.startingCash.value,
                                  varName     = 'ifNoPurchase',
                                  label       = '$ if no purchase made',
                                  helpText    = 'Amount of savings if home '
                                                'was not purchased'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'rentalIncome',
                                  label       = 'Rental income',
                                  helpText    = 'Monthly rental income'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'cRentalIncome',
                                  label       = 'Cum. rental income',
                                  helpText    = 'Total cumulative amount '
                                                'of income from renting'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'totalAmountPaid',
                                  label       = 'Total amount paid',
                                  helpText    = 'Total cumulative amount '
                                                'paid to mortgage'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.downPayment.value + \
                                                self.originationFees.value,
                                  varName     = 'totalAmountSpent',
                                  label       = 'Total amount spent',
                                  helpText    = 'Total cumulative amount '
                                                'spent on down payment '
                                                ' and mortgage'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.startingCash.value,
                                  varName     = 'totalSavings',
                                  label       = 'Total Savings',
                                  helpText    = 'Total cumulative amount '
                                                'paid to mortgage'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = 0.0,
                                  varName     = 'netWorth',
                                  label       = 'Net Worth after House Sale',
                                  helpText    = 'How much money you would have '
                                                'if you sold your house now'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.downPayment.value + \
                                                self.allPurchaseFees.value,
                                  varName     = 'tvmCost',
                                  label       = 'TVM Mortgage Cost',
                                  helpText    = 'The total cost of your '
                                                'mortgage in time-value money'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.downPayment.value + \
                                                self.allPurchaseFees.value,
                                  varName     = 'tvmCost',
                                  label       = 'TVM Mortgage Cost',
                                  helpText    = 'The total cost of your '
                                                'mortgage in time-value money'))
    self.addAttribute(mCostVector(parent      = self,
                                  value       = self.allPurchaseFees.value,
                                  varName     = 'livingCost',
                                  label       = 'Living Cost',
                                  helpText    = 'The TVM Cost of living in your '
                                                'house after selling'))
    
    if self.inflationRate.value != 0:
      self.inflationString = ' (inflation corrected)'
    else:  
      self.inflationString = ''
    
    # Introduce some shorthand for making calculations
    m    = self.paymentsPerYear.value
    PI   = self.monthlyPayment.value
    PR   = self.rentalPayment.value
    I    = self.interestPayment.data
    P    = self.principalPayment.data
    L    = self.loanSize.data
    H    = self.houseValue.data
    TI   = self.tPlusI.data
    M    = self.ifNoPurchase.data
    RI   = self.rentalIncome.data
    RC   = self.cRentalIncome.data
    A    = self.totalAmountPaid.data
    AD   = self.totalAmountSpent.data
    W    = self.netWorth.data
    S    = self.savings.data
    Y    = self.timeVector.data
    TC   = self.tvmCost.data
    LC   = self.livingCost.data
    rr   = self.rentalIncome.value
    rM   = self.mortgageRate.cRate
    rTVM = self.tvmRate.cData
    fTVM = self.tvmRate.fData
    rA   = self.appreciationRate.cRate
    rT   = self.taxRate.cRate
    rI   = self.insuranceRate.cRate
    #rD   = self.inflationRate.cRate #"D" is for the depreciation of money

    for i in range(1,self.numDataPoints.value):
      # j is the index of the beginning of the year, when 
      # rent/tax/insurance values are recalculated (for 
      # m = 12 payments per year)
      j = i - i%int(m)
      # Calculate tvm factor from beginning to present (prob need to refactor this)
      fTVMnow = (1.0+fTVM[0])**i
      # Calculate the interest accrued this month
      I[i] = L[i-1]*rM
      # Portion of monthly payment that pays down principal
      P[i] = PI - I[i]
      # Calculate the new loan amount after payment
      L[i] = L[i-1] - P[i]
      # Calculate appreciation in home value
      H[i] = H[i-1]*(1+rA)
      # Calculate cumulative payments to tax and insurance
      TI[i] = TI[i-1] + H[j]*(rT+rI)
      # Calculate savings if home had not been bought
      M[i] = M[i-1]*(1 + rTVM[i])
      # Calculate rental income
      RI[i] = H[j]*rr
      RC[i] = RC[i-1] + RI[i]
      # Calculate total amount paid to mortgage company or landlord
      A[i] = A[i-1] + PI + PR
      AD[i] = AD[i-1] + PI/fTVMnow
      # Calculate Savings
      S[i]  = (S[i-1]*(1+rTVM[i]) - PI - PR) - H[j]*(rT+rI) + RI[i]
      
      # Add contributions to TVM cost, factored by TVM factor
      TC[i] = TC[i-1] + PI/fTVMnow + PR/fTVMnow
      # Calculate cost of living in house if sold now (add TVM of loan, subtract tvm proceeds from house sale)
      LC[i] = TC[i] + (L[i] - \
              H[i]*(1 - self.listingFee.value)*(1 - self.capitalGainsTax.value*(Y[i]<self.capitalGainsPeriod.value)))/fTVMnow
    
    
    # Last loan size number is usually off from zero by a small amount due
    # to numerical precision.  Set it to zero here
    L[-1] = 0.0
    # After all is done, we can calculate our net worth over the mortgage,
    # which tells us how much we would have if we sold the home
    self.netWorth.data = RC + S - L + \
      H*(1 - self.listingFee.value)*(1 - self.capitalGainsTax.value*(Y<2.0))
    
    self.inflationCorrect()
    
   
  def inflationCorrect(self):
    for field in self.fieldList:
      field.inflationCorrect(monthlyInflationRate = self.inflationRate.fRate)
  
  # method for turning off all plots, to be called prior to turning on plots
  def setAllPlotsOff(self):
    for field in self.fieldList:
      field.plotThis = False
 
  # method for plotting all our costs
  def plotCosts(self,
                plotTitle = None):
    self.setAllPlotsOff() # change all plotThis's to False
    self.loanSize.plotThis           = True
    self.savings.plotThis            = True
    self.houseValue.plotThis         = True
    self.netWorth.plotThis           = True
    self.totalAmountPaid.plotThis    = True
    self.tPlusI.plotThis             = True
    self.cRentalIncome.plotThis      = True
    self.ifNoPurchase.plotThis       = True
    self.tvmCost.plotThis            = True
    self.livingCost.plotThis         = True
    if plotTitle is None:
      plotTitle = 'All costs'
    self.plotL(plotTitle=plotTitle)
  
  # method for creating and displaying a plot
  # TODO: axis labels
  def plotL(self,
            plotTitle = None,
            xAxisTitle = 'time [years]',
            yAxisTitle = 'value [$]'):
    configure_plotly_browser_state()
    data = []
    for field in self.fieldList:
      if field.plotThis is True:
        data.append(go.Scatter(x    = self.timeVector.data,
                               y    = field.data,
                               name = field.label))
    layout = go.Layout(
      title = plotTitle,
      xaxis = dict(
        title = xAxisTitle,
      ),
      yaxis = dict(
        title = yAxisTitle + self.inflationString,
        hoverformat = '.3g',
      ),
    )
    fig = go.Figure(data=data,layout=layout)
    py.plot(fig)
    
  def plot(self,*attributes):
    configure_plotly_browser_state()
    #if plotTitle is None:
    plotTitle = ' '
    #for mortgage in mortgages:
    #  mortgage.setAllPlotsOff()
    #  for attribute in attributes:
    #    getattr(mortgage,attribute).plotThis = True
    
    self.data = []
    for a,attribute in enumerate(attributes):
      self.data.append(
        go.Scatter(
          x = self.timeVector.data,
          y = getattr(self,attribute).data,
          name = getattr(self,attribute).label,
        )
      )
    layout = go.Layout(
      title = plotTitle,
      yaxis = dict(
        hoverformat = '.3g'
      )
    )
    
    fig = go.Figure(data=self.data,layout=layout)
    py.iplot(fig)
