# Base class for Mortgage() and MortgageComparison()
# Includes methods of setting defaults and printing
# attributes        
class MortgageBase:
  # Takes a dict of inputOptions replaces all default options with inputOptions
  # and returns a full list of options
  def populateOptions(self,kind,**inputOptions):
    options = MortgageOptions(kind,**inputOptions)
    self.options = options.options
    return self.options
    
  def displayOptions(self):
    for key,val in self.options.items():
      print('{} = {}'.format(key,val))
    
  def addData(self):
    self.goData = []
    for field in self.fieldList:
      if field.plotThis is True:
        self.goData.append(
          go.Scatter(
            x = self.timeVector.data,
            y    = field.data,
            name = field.label,
          )
        )
  
  def plot(self,plotTitle):
    configure_plotly_browser_state()
    
    layout = go.Layout(
      title = plotTitle,
      yaxis = dict(
        hoverformat = '.3g'
      )
    )
    fig = go.Figure(data=self.goData,layout=layout)
    py.iplot(fig)
  
