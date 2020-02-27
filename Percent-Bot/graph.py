import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime

# create data
y = [ 470.00, 530.33, 657.33, 529.83, 363.83]
x = ["02/17/2020", "02/18/2020", "02/19/2020", "02/20/2020", "02/21/2020"]

# plot
plt.plot(x,y)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Dollar Amount', fontsize=16)
plt.title('QQQ Call Option Earnings')
plt.gcf().autofmt_xdate()
plt.savefig('QQQ-Earnings.png')
plt.show()