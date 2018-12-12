class Times:

    def __init__(self):
        self.excecution = []
        self.cut = []
        self.air = []
    
    def addTimes(self, ex, cut, air):
        self.excecution.append(ex)
        self.cut.append(cut)
        self.air.append(air)
    
    def get_excecution(self):
        return self.excecution
    
    def get_cut(self):
        return self.cut
    
    def get_air(self):
        return self.air