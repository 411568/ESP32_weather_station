import pandas as pd
from pmdarima import auto_arima

df =   pd.read_csv("https://bit.ly/udemy_df",
              index_col = "Date",
              parse_dates = True).asfreq("D")
df.head()
print(df)

training = df.iloc[-100:-31,:]
test = df.iloc[-31:, :]

#SARIMA model
model = auto_arima(y = training.Udemy,
                   m = 7)


#Predictions
predictions = pd.Series(model.predict(n_periods = len(test)))
predictions.index = test.index
print(predictions[:5])

#Visualization
training['Udemy']['2020-01-01':].plot(figsize = (12,8), legend = True)
test['Udemy'].plot( legend = True)
predictions.plot(legend = True)