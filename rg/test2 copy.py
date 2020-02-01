import pandas as pd 
  
# Creating the dataframe  
df = pd.read_csv("data.csv") 

print(f'finsihed read in the file')
print (df)
# sum over the column axis. 
totalAmount = df['Amount'].sum()
print(totalAmount)

df['Percent'] = pd.eval('df.Amount/totalAmount*100')
print (df)
df.to_csv(r'percentage.csv')