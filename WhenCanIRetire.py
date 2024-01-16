# <GPLv3_Header>
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# \copyright
#                    Copyright (c) 2024 Nathan Ulmer.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <\GPLv3_Header>

##
# \mainpage Retirement Simulator
#
# \copydoc main.py

##
# \file WhenCanIRetire.py
#
# \author Nathan Ulmer
#
# \date \showdate "%A %d-%m-%Y"
#
# \brief A very basic finance simulation which simulates the median person's life until the median retirement age to
# tell them if they can retire. They can't, but my math could be wrong.
#
# \par You can modify the user inputs to see how it compares to your personal retirement plan. the only dependencies are
#  matplotlib and numpy.
#
# \todo Add major purchases - eg: Home, medical, etc
# \todo Account for social security payout - or expected payout given some expectation it won't exist when you retire?
# \todo Needs validation against some other retirement calculator / first principles calculation.



## \section Dependencies
import numpy
import matplotlib.pyplot as plt
import math
import time

## \section User Inputs
numMonteCarlos = 1000

startingYear = 2023
startingAge = 20

startingMonthlyExpenses = numpy.random.normal(2800,0,numMonteCarlos) # https://www.nerdwallet.com/article/finance/monthly-expenses-single-person-family
startingPay = numpy.random.normal(32500,2000,numMonteCarlos) # https://www.fool.com/the-ascent/research/average-us-income/#:~:text=The%20median%20U.S.%20income%20in,median%20female%20salary%20of%20%2436%2C726.
                                                             # https://fortune.com/2022/09/07/median-salary-gen-z-every-us-state/\

startingSavings = [0]*numMonteCarlos #numpy.random.normal(xxxx,xxxx,numMonteCarlos)

#######################################################################################################################



## \section CONSTANTS
percent = 1/100         # convert to percent
mpy = 12                # Months per year
numpy.random.seed(1234) # Master Seed

### GENZ STATS AND FUTURE ESTIMATES
expectedYearlyMonthlyExpenseCreep = numpy.random.normal(0.01,0.001/3,numMonteCarlos)  # Assume that your expenses will grow by an average of 1% on top of inflation
lifeExpectancy = numpy.random.normal(77,8,numMonteCarlos)                                   # Life expectancy and std deviation - per google
expectedYearlyInflationRate = numpy.random.normal(3.22*percent,1.5*percent,numMonteCarlos)  # Expected yearly inflation (rule of thumb) - probably an underestimate, lmao
expectedYearlyPayCOLA = numpy.random.normal(3*percent,0*percent/2,numMonteCarlos)           # Cost of Living Adjustment (raise)
incomeTaxRate = 22*percent                                                                  # Estimate
annualizedInvestmentReturnRate = numpy.random.normal(5*percent,2*percent,numMonteCarlos) # https://www.abovethecanopy.us/sequence-of-returns-biggest-risk-to-a-successful-retirement/



def retireAtAge(age,n,fig,axes):
    lifeExpectancy_ = int(math.ceil(lifeExpectancy[n]))
    expectedYearlyInflationRate[n] = max(0.0,expectedYearlyInflationRate[n])
    expectedRetirementAge = age

    NAYP = [startingPay[n]] # Non Adjusted Yearly Pay - Base Yearly pay without adjusting for cost of living
    NAYE = [startingMonthlyExpenses[n]*mpy] # Non Adjusted Yearly Expenses - Base yearly expennses without adjdusting for inflation
    NNetPay = [NAYP[0]*(1-incomeTaxRate) - NAYE[0]]
    NSav = [startingSavings[n] + NNetPay[0]] # Non Adjusted Savings at the end of the year

    AYP = [startingPay[n]] # Adjusted Yearly Pay - adjusted for COLA
    AYE = [startingMonthlyExpenses[n]*mpy] # Adjusted Yearly Expenses - adjusted for inflation
    NetPay = [AYP[0]*(1-incomeTaxRate) - AYE[0]]
    Sav = [startingSavings[n] + NetPay[0]]  # Non Adjusted Savings at the end of the year
    Invest = [Sav[0]]

    YearVec = [startingYear]

    for year in range(1,lifeExpectancy_-startingAge+1):
        YearVec.append(year+startingYear)

        if(year+startingAge <= expectedRetirementAge):
            NAYP.append(startingPay[n])
        else:
            NAYP.append(0.0)

        NAYE.append(startingMonthlyExpenses[n]*mpy)
        NNetPay.append(NAYP[year]*(1-incomeTaxRate) - NAYE[year])
        NSav.append(NSav[year-1]+NNetPay[year])

        if (year + startingAge <= expectedRetirementAge):
            AYP.append(AYP[year-1]*(1+expectedYearlyPayCOLA[n]))
        else:
            AYP.append(0.0)
        AYE.append(AYE[year-1]*(1+expectedYearlyInflationRate[n]+expectedYearlyMonthlyExpenseCreep[n]))
        NetPay.append(AYP[year]*(1-incomeTaxRate)-AYE[year])
        Sav.append(Sav[year-1]+NetPay[year])
        Invest.append((Invest[year-1]+NetPay[year]) * (1+annualizedInvestmentReturnRate[n]))


    '''
    fig,axes = plt.subplots(2,2)
    axes[0][0].plot(YearVec, NAYP)
    axes[0][0].set_xlabel("Year")
    axes[0][0].set_ylabel("Non-adj Yr Pay ($,%s)"%startingYear)
    axes[0][0].grid()
    axes[1][0].plot(YearVec,NAYE)
    axes[1][0].set_xlabel("Year")
    axes[1][0].set_ylabel("Non-adj Yr Expenses ($,%s)"%startingYear)
    axes[1][0].grid()
    axes[0][1].plot(YearVec, NNetPay)
    axes[0][1].set_xlabel("Year")
    axes[0][1].set_ylabel("Non-adj Yr Net ($,%s)"%startingYear)
    axes[0][1].grid()
    axes[1][1].plot(YearVec, NSav)
    axes[1][1].set_xlabel("Year")
    axes[1][1].set_ylabel("Nonadjusted Total Savings($)")
    axes[1][1].grid()
    '''

    if(Invest[lifeExpectancy_ - startingAge] >= 10000):
        '''
        axes[0][0].plot(YearVec, AYP)
        axes[0][0].set_xlabel("Year")
        axes[0][0].set_ylabel("adj Yr Pay ($)")
        axes[0][0].grid()
        axes[1][0].plot(YearVec, AYE)
        axes[1][0].set_xlabel("Year")
        axes[1][0].set_ylabel("adj Yr Expenses ($)")
        axes[1][0].grid()
        axes[0][1].plot(YearVec, NetPay)
        axes[0][1].set_xlabel("Year")
        axes[0][1].set_ylabel("adj Yr Net ($)")
        axes[0][1].grid()
        axes[1][1].plot(YearVec, Sav)
        axes[1][1].set_xlabel("Year")
        axes[1][1].set_ylabel("Total Savings (non-Invested($))")
        axes[1][1].grid()
        axes[2][1].plot(YearVec, Invest)
        axes[2][1].set_xlabel("Year")
        axes[2][1].set_ylabel("Total Savings (Invested($))")
        axes[2][1].grid()
        '''
        return True
    else:
        #plt.show()
        return False


if __name__ == '__main__':
    startTime = time.time()
    lastTime = startTime
    print("This program calculates your expected retirement finances")

    maxAge = 100
    retiredAt = []
    fig, axes = plt.subplots(1,1)
    for n in range(numMonteCarlos):
        if(time.time() - lastTime > 20): # Every x seconds, print the current runtime
            lastTime = time.time()
            print("Running for %ss: %s montecarlos complete"%((time.time()-startTime),n))
        age = maxAge

        while(retireAtAge(age,n,fig,axes)):
            age = age - 1
        retiredAt.append(age)

    print("Running for %ss: %s montecarlos complete" % ((time.time() - startTime), n))

    print("=================================================")
    print("=================================================")
    print("Number of MonteCarlo Runs:", len(retiredAt))
    print("mean retire age: ",numpy.mean(retiredAt))
    print("median retire age: ", numpy.median(retiredAt))
    #print("mode retire age: ", numpy.mode(retiredAt))
    print("min retire age: ", numpy.min(retiredAt))
    count = 0
    for lifeTime in retiredAt:
        if lifeTime == maxAge:
             count = count + 1
    print("count no retire: ", count)
    print("pct no retire: %0.1d"% (count/len(retiredAt)*100), "%")
    plt.figure(1)
    plt.scatter(range(numMonteCarlos),retiredAt)
    plt.grid()
    plt.title("Possible Retired Age Scatter Plot")

    fig2, axes2 = plt.subplots(1,2)
    axes2[0].hist(retiredAt,50)
    axes2[0].grid()
    # plot the cumulative histogram
    n, bins, patches = axes2[1].hist(retiredAt, 65, density=True, histtype='step', cumulative=True, label='Empirical')
    axes2[1].grid()
    plt.title("Retired Age Histogram and CDF")
    plt.show()


# <GPLv3_Footer>
################################################################################
#                      Copyright (c) 2024 Nathan Ulmer.
################################################################################
# <\GPLv3_Footer>