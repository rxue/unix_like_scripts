# initialization of project in Ubuntu
## Pre-requisite
* `venv` is assumed to be built-in
Action: my local is `python3.12` => need `sudo apt-get install python3.12-venv`

# Knowledge crunching on tax calculation
## transaction type knowledge
* Laji=700 - selitys: NOSTO. e.g. payment of buying stocks
### Laji=710 - Selity=ARVOPAPERIT
#### Dividend
Example Viesti:

 OP Säilytys Oy                     OCCIDENTAL PETROLEUM ORD SHS       US6745991058                       Osinkotuotto                       Osinko        0,24          USD/KplOmistettu määrä             75Kpl  Tuoton määrä               18,00USDLähdevero  US15,0   %       2,70USDVal.kurssi                1,1704

Analysis: 

Dividend is 0,24 USD/share, there are 75 shares in the portfolio => 75 * 0,24 = 18 (USD)

15,0% tax-at-source => 18 * 0.15 = 2.7 (USD) tax-at-source

What is left to account is: 18-2.7 = 15.3 (USD)

EURO:USD currency rate = 1.1704 => What is 15.3/1.1704 = 13.07



* Laji=730 - Selity=PALVELUMAKSU

## Asset
Examples:
* stock shares of companies
