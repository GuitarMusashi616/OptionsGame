
import datetime
import QuantLib as ql
from matplotlib import pyplot as plt

def binomial_price(option, bsm_process, steps):
    binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
    option.setPricingEngine(binomial_engine)
    # price = option.NPV()
    return option

def just_option_stats(american_option, bsm_process):
    return binomial_price(american_option, bsm_process, 200)

def graph_option_cost(american_option, bsm_process):
    steps = range(2, 200, 1)
    prices = [binomial_price(american_option, bsm_process, step) for step in steps]

    fig, ax = plt.subplots()
    ax.plot(steps, prices, label="Binomial Tree Price", lw=2, alpha=0.6)
    # ax.plot([0,200],[bs_price, bs_price], "--", label="BSM Price", lw=2, alpha=0.6)
    ax.set_xlabel("Steps", size=14)
    ax.set_ylabel("Price", size=14)
    ax.set_title("Binomial Tree Price For Varying Steps", size=14)
    ax.legend()
    return prices[-1]

def option_price(
        calculation_date: datetime.date,
        maturity_date: datetime.date,
        spot_price: float,
        strike_price: float,
        volatility: float,
        dividend_rate: float,
        is_call: bool,
        risk_free_rate: float
    ):

    maturity_date = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
    calculation_date = ql.Date(calculation_date.day, calculation_date.month, calculation_date.year)
    option_type = ql.Option.Call if is_call else ql.Option.Put

    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

    ql.Settings.instance().evaluationDate = calculation_date

    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    settlement = calculation_date
    am_exercise = ql.AmericanExercise(settlement, maturity_date)
    american_option = ql.VanillaOption(payoff, am_exercise)

    spot_handle = ql.QuoteHandle(
        ql.SimpleQuote(spot_price)
    )
    flat_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(
        calculation_date, 
        risk_free_rate, 
        day_count)
    )
    dividend_yield = ql.YieldTermStructureHandle(
    ql.FlatForward(
        calculation_date, 
        dividend_rate, 
        day_count)
    )
    flat_vol_ts = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(
        calculation_date, 
        calendar, 
        volatility, 
        day_count)
    )
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, 
                                    dividend_yield, 
                                    flat_ts, 
                                    flat_vol_ts)

    return just_option_stats(american_option, bsm_process)


if __name__ == "__main__":
    calc_date = datetime.date(2015, 5, 8)
    maturity_date = datetime.date(2016, 1, 15)
    price = option_price(calc_date, maturity_date, 127.62, 130, 0.20, 0.0163, True, 0.001)
    print(price)
