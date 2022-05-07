import math
import numpy as np
from scipy.stats import norm


class EuropeanCall:

    def call_delta(self, spot, vol, strike,expiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log(spot/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        return z1

    def call_gamma(self, spot, vol, strike,expiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log(spot/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z2 = z1/(spot*vol*math.sqrt(expiry))
        return z2

    def call_vega(self, spot, vol, strike,expiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log(spot/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z2 = spot*z1*math.sqrt(expiry)
        return z2/100

    def call_price(self, spot, vol, strike,expiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log(spot/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z1 = z1*spot
        x2 = math.log(spot/(b*strike)) - .5*(vol*vol)*expiry
        x2 = x2/(vol*(expiry**.5))
        z2 = norm.cdf(x2)
        z2 = b*strike*z2
        return z1 - z2

    def __init__(self, spot, vol, strike,expiry, rf):
        self.spot = spot
        self.vol = vol
        self.strike = strike
        self.expiry = expiry
        self.rf = rf
        self.price = self.call_price(spot, vol, strike, expiry, rf)
        self.delta = self.call_delta(spot, vol, strike, expiry, rf)
        self.gamma = self.call_gamma(spot, vol, strike, expiry, rf)
        self.vega = self.call_vega(spot, vol, strike, expiry, rf)


class EuropeanPut:

    def put_delta(elf, spot, vol, strike,xpiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log(spot/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        return z1 - 1

    def put_gamma(self, spot, vol, strike,expiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log(spot/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z2 = z1/(spot*vol*math.sqrt(expiry))
        return z2

    def put_vega(self, spot, vol, strike,expiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log(spot/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z2 = spot*z1*math.sqrt(expiry)
        return z2/100

    def put_price(self, spot, vol, strike,expiry, rf):
        b = math.exp(-rf*expiry)
        x1 = math.log((b*strike)/spot) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z1 = b*strike*z1
        x2 = math.log((b*strike)/spot) - .5*(vol*vol)*expiry
        x2 = x2/(vol*(expiry**.5))
        z2 = norm.cdf(x2)
        z2 = spot*z2
        return z1 - z2

    def __init__(self, spot, vol, strike,expiry, rf):
        self.spot = spot
        self.vol = vol
        self.strike = strike
        self.expiry = expiry
        self.rf = rf
        self.price = self.put_price(spot, vol, strike, expiry, rf)
        self.delta = self.put_delta(spot, vol, strike, expiry, rf)
        self.gamma = self.put_gamma(spot, vol, strike, expiry, rf)
        self.vega = self.put_vega(spot, vol, strike, expiry, rf)


call = EuropeanCall(543, .53, 545, 30/365, .015)
print("Valeur de L'option: \n",call.price*1000)
print("\n")
print("Delta Call: ",call.delta*-1000)
print("Gamma Call: ",call.gamma*-1000)
print("vega Call : ",call.vega*-1000)
print("\n")

call_a = EuropeanCall(543, .53, 550, 30/365, .015)
print("Valeur de L'option A: \n",call_a.price)
print("\n")
print("Option A:")
print("Delta Call : ",call_a.delta)
print("Gamma Call: ",call_a.gamma)
print("Vega Call: ",call_a.vega)
print("\n")

call_b = EuropeanCall(543, .53, 555, 30/365, .015)
print("Valeur de L'option B: \n",call_b.price)
print("\n")
print("Option B:")
print("Delta Call: ",call_b.delta)
print("Gamma Call: ",call_b.gamma)
print("Vega Call: ",call_b.vega)
print("\n")

greeks = np.array([[call_a.gamma, call_b.gamma], [call_a.vega, call_b.vega]])
portfolio_greeks = [[call.gamma*1000], [call.vega*1000]]

inv = np.linalg.inv(np.round(greeks, 2))
print("inverse matrix: \n",inv)
print("\n")

w = np.dot(inv, portfolio_greeks)
print("Montant D'allocation pour les Option A et B: \n",w)
print("\n")

print("Neutralité de gamma and vega: \n")
print(np.round(np.dot(np.round(greeks, 2), w) - portfolio_greeks))
print("\n")


portfolio_greeks = [[call.delta*-1000], [call.gamma*-1000], [call.vega*-1000]]
greeks = np.array([[call_a.delta, call_b.delta], [call_a.gamma, call_b.gamma], [call_a.vega, call_b.vega]])
print(np.round(np.dot(np.round(greeks, 2), w) + portfolio_greeks))
print("\n")

print("Verification de la Neutralité de notre portefeuille: \n")
long_nvda = [[46], [0], [0]]
print(np.round(np.dot(np.round(greeks, 2), w) + portfolio_greeks + long_nvda))
print("\n")
