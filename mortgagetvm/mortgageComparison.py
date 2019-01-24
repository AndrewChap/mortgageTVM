class MortgageComparison(MortgageBase):
  def __init__(self, kind = None, *mortgages):
    
    self.options = self.populateOptions(kind = kind)
    #def __init__(self,**options):
    #self.options = self.populateOptions(**options)  # set default attributes
    #self.setAttributes(self.options)
    
    # Create empty list of mortgages
    self.mortgages = []
    
    # add each input mortgage to list of mortgages
    for mortgage in mortgages:
      self.addMortgage(mortgage=mortgage)

    # create default colors and dash styles
    self.dashCycle = [None,'dash','dot','dashdot']
    self.colorCycle = ['rgb(205,  12,  24)',
                       'rgb( 42, 202,  24)',
                       'rgb(205,  12, 224)',
                       'rgb(100, 100,  14)',
                       'rgb(  0, 130, 100)']
    

  def setDefaults(self,**defaults):
    for key,val in defaults.items():
      self.options[key] = val

  
 # "base" mortgage adding, with default options     
  def addMortgage(self,
                  kind = None,
                  mortgage = None,
                  **options):
    # If no input mortgage, we need to create it from **options dict
    if mortgage is None:
      mortgageAttributes = self.options.copy() # start with defaults
      for key,val in options.items():           # replace default vals
        mortgageAttributes[key] = val           # with defined options
      #pdb.set_trace()
      mortgage = Mortgage(**mortgageAttributes)
    # If the mortgage has no name, give it a generic name
  
    if mortgage.name is None:
      mortgage.name = 'mortgage{}'.format(len(self.mortgages)+1)
    # If no label is given, default to the name
    if mortgage.label is None:
      mortgage.label = mortgage.name
    # Add the mortgage to the mortgage list
    #pdb.set_trace()
    self.mortgages.append(mortgage)
    
  def addRental(self,**options):
    self.addMortgage(kind='rental',**options)
  
  def addInvestmentProperty(self,**options):
    self.addMortgage(kind='investmentProperty',**options)
    
 
  def simulateMortgages(self):
    for mortage in self.mortgages:
      mortage.simulateMortgage()
  def plot(self,*attributes):
    configure_plotly_browser_state()
    #if plotTitle is None:
    plotTitle = 'Comparison'
    #for mortgage in mortgages:
    #  mortgage.setAllPlotsOff()
    #  for attribute in attributes:
    #    getattr(mortgage,attribute).plotThis = True
    #pdb.set_trace()
    
    self.data = []
    for a,attribute in enumerate(attributes):
      for m,mortgage in enumerate(self.mortgages):
        self.data.append(
          go.Scatter(
            x = mortgage.timeVector.data,
            y = getattr(mortgage,attribute).data,
            name = mortgage.label + ': ' + getattr(mortgage,attribute).label,
            line = dict(
              dash = self.dashCycle[a],
              color = self.colorCycle[m],
            )
          )
        )
    layout = go.Layout(
      title = plotTitle,
      yaxis = dict(
        hoverformat = '.3g'
      )
    )
    
    #pdb.set_trace()
    fig = go.Figure(data=self.data,layout=layout)
    py.plot(fig)
      
