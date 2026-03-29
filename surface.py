
import yfinance as yf
import matplotlib.pyplot as plt
import inspect
import numpy as np
from datetime import datetime
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D


data = yf.Ticker('SPY')

spot_price = data.info['regularMarketPrice']


# needed lists to for plot
expirations = {}

iv_all = []
time = []
plot_strikes = []

dates = list(data.options)


#making list of all expirations and their time to expiration in days, filtering out those that are too close or too far from expiration

for exp in dates:
  data_exp = datetime.strptime(exp, '%Y-%m-%d')

  if (data_exp - datetime.today()).days <= 60 and (data_exp - datetime.today()).days > 10:
    expirations[exp] = (datetime.strptime(exp, '%Y-%m-%d') - datetime.today()).total_seconds() / 86400


#making list of all strikes for calls and puts, filtering out those that are too far from the spot price
calls = data.option_chain().calls

all_strikes = calls[(calls['strike'] > spot_price * 0.95) & (calls['strike'] < 1.2 * spot_price)]['strike'].tolist()

#mfilling lists

print('DONE WITH PREPPARING DATA, MOVING ONTO FILLING LISTS FOR PLOTTING')

##################################O
#Original way, more api calls

# for strike in all_strikes:
#   print(f'NOW DOING {strike}')

#   for exp, time_to_exp in expirations.items():
#     iv = -1
#     call_table = data.option_chain(exp).calls
#     put_table = data.option_chain(exp).puts
#     table = call_table if strike >= spot_price else put_table
    
#     if len(table[table['strike'] == strike]) > 1:
#       iv = table[table['strike'] == strike].iloc[0]['impliedVolatility'].item()
#     elif len(table[table['strike'] == strike]) == 1:
#       iv = table[table['strike'] == strike]['impliedVolatility'].item()
#     else:
#       continue

#     if iv >= 0:
#         time.append(time_to_exp)
#         iv_all.append(iv)
#         plot_strikes.append(strike)

#More efficeint way
chains = {exp: data.option_chain(exp) for exp in expirations}

for exp, time_to_exp in expirations.items():
    call_table = chains[exp].calls
    put_table = chains[exp].puts

    for strike in all_strikes:
        table = call_table if strike >= spot_price else put_table
        filtered = table[table['strike'] == strike]

        if len(filtered) == 0:
            continue
        
        iv = filtered.iloc[0]['impliedVolatility']

        if iv >= 0:
            time.append(time_to_exp)
            iv_all.append(iv)
            plot_strikes.append(strike)


#plotting the surface

time_unique = np.unique(time)
strikes_unique = np.unique(plot_strikes)

Time, Strikes = np.meshgrid(time_unique, strikes_unique)

IV = griddata((time, plot_strikes), iv_all, (Time, Strikes), method='linear')


iv_surface = plt.figure(figsize=(16,9))
iv_surface.patch.set_facecolor('#0b0d0f')

ax = iv_surface.add_subplot(111, projection='3d')
ax.set_facecolor('#0b0d0f')

ax.plot_surface(Time, Strikes, IV, edgecolor = 'white', cmap='magma', lw=.1, alpha=.9)
ax.set_title('IV Surface', color='white', fontsize = 16)
ax.set_xlabel('Time', color='white')
ax.set_ylabel('Strike', color='white')
ax.set_zlabel('IV', color='white')
ax.tick_params(colors='white')
plt.show()




################################
#Old way just calls

# for exp, time_to_exp in expirations.items():
#   if time_to_exp >= 0:
#     calls_table = data.option_chain(exp).calls
#     puts_table = data.option_chain(exp).puts

#     for index, row in table.iterrows():
      
      
#       strike, iv = row['strike'], row['impliedVolatility']

#       if iv >= 0 and strike > spot_price and strike < 1.15 * spot_price:
#         time.append(time_to_exp)
#         strikes.append(strike)
#         iv_all.append(iv)