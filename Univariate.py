import pandas as pd
import numpy as np

class Univariate():
    
    def quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            if(dataset[columnName].dtypes=='O'):
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan,qual
    
    def freqTable(coloumnName,dataset):
        freqTable=pd.DataFrame(columns=["Unique_values","Frequency","Relative_Frequency","cumsum"])
        freqTable["Unique_values"]=dataset[coloumnName].value_counts().index
        freqTable["Frequency"]=dataset[coloumnName].value_counts().values
        freqTable["Relative_Frequency"]=freqTable["Frequency"]/103
        freqTable["cumsum"]=freqTable["Relative_Frequency"].cumsum()
        return freqTable
    
    def Univariate(dataset,quan):
        desprictive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5rule","Lesser","Greater","Min","Max"],columns=quan)
        for coloumnName in quan:
            desprictive[coloumnName]["Mean"]=dataset[coloumnName].mean()
            desprictive[coloumnName]["Median"]=dataset[coloumnName].median()
            desprictive[coloumnName]["Mode"]=dataset[coloumnName].mode()[0]
            desprictive[coloumnName]["Q1:25%"]=dataset.describe()[coloumnName]["25%"]
            desprictive[coloumnName]["Q2:50%"]=dataset.describe()[coloumnName]["50%"]
            desprictive[coloumnName]["Q3:75%"]=dataset.describe()[coloumnName]["75%"]
            desprictive[coloumnName]["99%"]=np.percentile(dataset[coloumnName],99)
            desprictive[coloumnName]["Q4:100%"]=dataset.describe()[coloumnName]["max"]
            desprictive[coloumnName]["IQR"]=desprictive[coloumnName]["Q3:75%"]-desprictive[coloumnName]["Q1:25%"]
            desprictive[coloumnName]["1.5rule"]=1.5*desprictive[coloumnName]["IQR"]
            desprictive[coloumnName]["Lesser"]=desprictive[coloumnName]["Q1:25%"]-desprictive[coloumnName]["1.5rule"]
            desprictive[coloumnName]["Greater"]=desprictive[coloumnName]["Q3:75%"]+desprictive[coloumnName]["1.5rule"]
            desprictive[coloumnName]["Min"]=dataset[coloumnName].min()
            desprictive[coloumnName]["Max"]=dataset[coloumnName].max()
        return desprictive
    
    def CheckOutliers(desprictive,quan):
        lesser=[]
        greater=[]

        for coloumnName in quan:
            if(desprictive[coloumnName]["Min"]<desprictive[coloumnName]["Lesser"]):
                lesser.append(coloumnName)
            if(desprictive[coloumnName]["Max"]>desprictive[coloumnName]["Greater"]):
                greater.append(coloumnName)
        return lesser,greater
    
    def ReplaceOutliers(desprictive,lesser,greater,dataset,quan):
        for coloumnName in lesser:
            dataset[coloumnName][dataset[coloumnName]<desprictive[coloumnName]["Lesser"]]=desprictive[coloumnName]["Lesser"]
        for coloumnName in greater:
            dataset[coloumnName][dataset[coloumnName]>desprictive[coloumnName]["Greater"]]=desprictive[coloumnName]["Greater"]
        desprictive=Univariate.Univariate(dataset,quan)
        lesser,greater=Univariate.CheckOutliers(desprictive,quan)
       
        return desprictive,lesser,greater
       
    

    

