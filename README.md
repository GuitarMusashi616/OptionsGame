# Stock / Option Trader Sim
## How to play

Type text into the console to trade stocks / options

## Commands

1. "info" - shows the current assets you're holding

2. "portval" - shows the current value of all assets you're holding

3. "check" - use to check the current price of an asset
    - eg. check tsla - will show the current price of tsla
    - eg. check 250 tsla call 2023 2 10 - show price of buying the call option with 250 strike and expiration of 2023 2 10

4. "graph" - use to see the price of the stock over time
    - eg. graph tsla - show a graph of tsla's price over the last year
    - eg. graph tsla 7 - show tsla's price over the last 7 days

4. "buy" - use to buy stocks / options
    - eg. buy 4 tsla
    - eg. buy 225 tsla put 2023 2 10

5. "sell" - use to sell stocks / options
    - eg. sell 4 aapl
    - eg. sell 400 spy call 2023 2 10

6. "next" - use to go forward in time
    - eg. next - go forward 1 week
    - eg. next 1 - go forward 1 day
    - eg. n 1 - go forward 1 day

7. "exit" - quit the simulator

## Install

1. git clone https://github.com/GuitarMusashi616/OptionsGame.git 
2. cd OptionsGame
3. pip install -r requirements.txt
4. py main.py