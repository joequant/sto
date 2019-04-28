# Basic distinction

* Negotiable tokens - If I have the bitcoin, I have the bitcoin

* Non-negotiable tokens - If I have the shares, and the issuers claims
  I don't have the shares, I have a big problem

# Base case for negotiable tokens

Cryptocurrencies.  User sends crypto to exchange via address.
Exchanges puts crypto into cold wallet.  Exchange changes ownership
and stores ownership internally.  Exchange returns tokens on request.
Exchange must track tokens.

# Case for traditional public securities

* Ownership data is done via brokers who are trusted to maintain
  information.  Brokers trade on exchange, and then undertake clearing
  and settlement process.

* Note that the record keeping process for public securities is vastly
  differnt from private securities.

# We are doing something fundamentally interesting

* Trading private companies on public exchanges (even if trading is
  restricted) is new and interesting

# STO's issues

* STO's are records of ownership - Good news since they aren't bearer tokens
* Access control, on-boarding off-boarding

# Questions

* How does issuer and exchange coordinate onboarding and client data?

* How does exchange deal with wallets which are whitelisted?

* What is the legal relationship between issuer and exchange?  In the
case of negotiable tokens, no legal relationship is necessary.  In
case of non-negotiable tokens some legal relationship is necessary
since issuer may not recognize exchange.

* How does the issuer stop trading or do upgrades?

* What happens in case of liquidation?  Note that one big difference
  between cryptoexchanges and securities exchanges is that securities
  exchanges do not have legal ownership of the assets.  If NYSE goes
  down, no one loses their assets.

# Regulators

* In private securities, regulator gets data from the issuer.  For
  public securities, regulator gets data from the exchange.  Who does
  the regulator go after?

# Possible models

* Exchange is legal owner of shares, and exchange participants are
  beneficial owners.  Problems: Really nasty problems in case exchange
  has to liquidate.  Issuer has no transparency into exchange.
  Exchange needs agreement with issuer to deal with white lists.  No
  use of blockchain technology to manage access.

* Exchange manages wallets of the users.  Problems: Need to figure out
  how the smart contracts work.

* Exchange does everything and manages tokens for issuer.  Problems;
  Issuer is highly dependent on exchange for everything.  Also issuer
  gets pulled into regulatory net of exchange.


# Recommendation

* Exchange is broker-dealer (type 1 HK license) for shares and holds
  the shares in trust for its customers.  Exchange signs agreement
  with issuer.  Exchange clients must be approved by issuer, and
  client can only move tokens into wallets that have been whitelisted
  by issuer.  Exchange will send issuer report of ownership daily.

  Unlike negotiable tokens in which the exchange creates a special
  wallet to get coins, the client of the exchange must provide a
  whitellisted wallet, and the exchange maintains one wallet for
  deposits and withdrawals.  A client can only send and receive tokens
  to their registered wallet, and the exchange will check to see if
  the wallet is still active before allowing a trade.

  The identification of the whitelisted wallet must match the
  identification of the owner on the exchange

* If we want to get really fancy, then the exchange and the issuer can
  communicate about a client through the wallet.