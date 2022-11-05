import pandas as pd

# Reading in data from CSV files from data folder into separate data frames
df = pd.read_csv("data\halloween2019a.csv", sep=',')
df1 = pd.read_csv("data\halloween2019b.csv", sep=',')
df2 = pd.read_csv("data\halloween2019c.csv", sep=',')
df3 = pd.read_csv("data\cemNames.csv", sep=',')

# Adjusting column names to match
df1 = df1.rename(columns={' LastName':'LastName',' DOB':'DOB',' DOD':'DOD',' Sex':'Sex'})

# Splitting Name column into FirstName and LastName
df2['Name'] = df2.Name.str.rsplit(' ',1)
df2[['FirstName','LastName']] = pd.DataFrame(df2.Name.tolist(), index= df2.index)
df2.drop('Name', axis=1, inplace=True)

# Removing all middle names/initials from FirstName column
listFirstMiddle = df2.FirstName.str.split(' ',1)
first = list()
for i in listFirstMiddle : 
    first.append(i[0])
df2['FirstName'] = first

# Merging unified data to one common data frame
df = pd.concat([df,df1,df2,df3],ignore_index=True)

# Removing unnecessary/inconsistent middle name column
df = df.drop('MiddleName',axis=1)

#Shorten sex column to (m,f,n) abbreviations
df['Sex'] = df['Sex'].astype(str).str[0]

#Shorten DOB and DOD to only include year
df['DOB'] = df['DOB'].astype(str).str[-4:]
df['DOD'] = df['DOD'].astype(str).str[-4:]

df = df.dropna(subset=['DOB','DOD'],how='any')


# Add column lifespan (DOD - DOB)
df['lifespan'] = df['DOD'].astype(int,errors='ignore') - df['DOB'].astype(int,errors='ignore')

print(df)
