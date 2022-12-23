import pandas as pd
import numpy as np
# Reading the data from file and cleaning any empty values from between rows
df = pd.read_csv("input.csv")
df = df.dropna()
df = df.reset_index(drop=True)
# Extracting columns from database and storing it.
customer = pd.DataFrame(df, columns=['Customer Id'])
customer = customer.rename(columns={'Customer Id': 'cid'})
date = pd.DataFrame(df, columns=['Date'])
transactions = pd.DataFrame(pd.DataFrame(df, columns=['Amount']))
# Intializing variables to calculate the max,min ,ending balance for the customers
today = []
id = []
dates = []
values = []
Minimum = []
Maximum = []
sum = 0
neg_sum = 0
max = -np.inf
min = np.inf
# Running the loop
for i in range(0, len(customer)):
    tod = date.Date[i]
    # str - Extracting the month for each customer.
    str = tod[0:2] + "-" + tod[len(tod) - 4:len(tod)]
    # Checking whether the date and customer is already in the list or not
    if str not in dates or customer.cid[i] not in id:
        id.append(customer.cid[i])
        dates.append(str)
        today.clear()
        today.append(tod)
        sum = sum-neg_sum
        if min > sum and i > 1:
            min = sum
        if max < sum and i > 1:
            max = sum
        values.append(sum)
        Minimum.append(min)
        Maximum.append(max)
        if transactions.Amount[i] < 0:
            neg_sum = abs(transactions.Amount[i])
            sum = 0
            min = transactions.Amount[i]
            max = transactions.Amount[i]
        else:
            sum = transactions.Amount[i]
            neg_sum = 0
            min = transactions.Amount[i]
            max = transactions.Amount[i]
    else:
        if tod not in today:
            sum = sum - neg_sum
            neg_sum = 0
            if sum > max:
                max = sum
            if sum < min:
                min = sum
            today.append(tod)
            if transactions.Amount[i] > 0:
                sum = sum + transactions.Amount[i]
            else:
                neg_sum = abs(transactions.Amount[i])
            print(customer.cid[i])

        else:
            if transactions.Amount[i] < 0:
                neg_sum = neg_sum + abs(transactions.Amount[i])
            else:
                sum = sum + transactions.Amount[i]
sum = sum - neg_sum
if sum > max:
    max = sum
if sum < min:
    min = sum
values.append(sum)
Maximum.append(max)
Minimum.append(min)
values.remove(0)
Maximum.remove(-np.inf)
Minimum.remove(np.inf)
outp = pd.DataFrame(np.column_stack([id, dates, Minimum, Maximum, values]),
                    columns=['CustomerID', 'MM/YYYY', 'MinBalance', 'MaxBalance', 'EndingBalance'])
outp.to_csv('output.csv')
