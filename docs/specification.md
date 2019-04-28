This document is intended to be PUBLIC.  There is a companion document
that contains additional private information

# Objective

Create minimal viable product to allow stakeholders to tokenize the
hedge funds in Hong Kong.  The target hedge funds are Regulation S
fund registered in Cayman Islands with offices in Hong Kong.  The fund
target has a small number of investors and the purpose of the
tokenization is to allow current investors trade between themselves.

The reason for tokenizing a fund is that the fund structure can be
used to tokenize any asset.  Once a fund is tokenized, then the fund
can have legal ownership of any asset or any pool of assets.  The
tokens will be non-negotiable and access control will be done with
white listing.  The tokens are intended to be P2P traded among
shareholders, and therefore can be traded without an exchange.

The project will be funded by a cyberport grant from Hong Kong.  The
Cyberport grant operates in six month reimbursement cycle with a
report to Cyberport at the end of six months.

The ultimate goal is to create an asset backed securitization
infrastructure for emerging markets and to allow for cross border
trading and settlement of securities, particularly among the members
of the Belt and Road initiative.

Currently, a person in the Philippines cannot purchase securities that
are orginated in Sri Lanka, unless those securities have been listed
in a public market in the US/UK, and unless both parties have
brokerage accounts.  With security tokens, the purchaser of tokens in
the Philippines can send the originator, bitcoin, and then originator
can send over security tokens.

This also allows for cross-border brokerage services.  Once everything
is tokenized, a client in Tanzania can connect with a broker in Hong
Kong that can arrange purchases of tokens.  Since the settlement
system is decentralized, the tokens are all recorded on the
blockchange and so neither party needs to be concerned with the
underlying settlement system.

Among the uses for this technology is to begin to trade and securitize
exotic products such as accounts receivables and trade finance
factoring.  The big target is to create money markets and mortgage
backed securities markets in China, India, Southeast Asia and Africa.

Currently only billion dollar markets can be securitized.  The goal of
this technology is to allow for securitizing of micro or nano markets.

# Schedule

* Phase one - Create minimal viable product (May to November)

** Technology infrastructure - Polymath ST20 tokens

*** Must have features
**** Ability for issuer to mint and retrieve tokens
**** Ability for issuer to white list tokens
**** Ability for issuer to stop trading and reissue tokens

*** Strech goals
**** Need to have mechanism to deal with stamp tax

** Legal infrastructure - Term of service agreement
** Trading infrastructure - P2P trading provided with market makers over
chat group

* Phase two - Refine token and productize assets

*** Separation of functions
*** Integrate with exchanges
*** Shared white list

** Reach out to NGO's and non-profits.  One bottleneck for this
   technology is that the deals are too small.  I'd like to securitize
   a USD 10k small business in Tanzania or grants in Hong Kong.

# Legal infrastructure

The legal infrastructure is simplified by the fact that we are not
tokenizing shares, we are tokenizing the share registry.  Because this
is fundamentally a technology change and not a change in the legal
structure of the fund, the legal costs should be minimal.

The legal documentation will consist of a terms of service agreement
between the issuer and the client.  The TOS agreement will be that the
issuer agrees to provide a service for the client to notify the issuer
of share transfers, and legally the tokens will be entries on the
share registry of the issuing company.

This legal mechanism should be valid in common law jurisdictions, and
it will be assumed that the operating law for the share transfers will
by BVI or Caymans.  Most civil law jurisdictions, such as Estonia,
have statutory requirements for transfer of shares so this mechanism
will not be viable there.

The one major issue is how to deal with Hong Kong stamp tax.  This
will likely be done with a locking mechanism that prevents additional
token transfers unless there is evidence that stamp tax has been paid.

# Technical infrastructure

## Polymath as platform
The technology platform is the ST20 tokenization system by Polymath.
The advantages of polymath are

* the code is open source
* there is a community of developers and the Polymath core team is extremely friendly and open

* Polymath is concerned only with the technology platform and not with
  providing legal infrastructure.  The problem with alternative
  business models is that many of them seek to provide all-in-one
  services, which then creates vendor lock-in and pulls you into
  jurisdictions such as the US or EU, that you want to stay out of.

* Many of the alternative products have a regulatory kill switch which
  allow regulators to stop the project through AML-KYC.  This is
  particularly a problem when you have a cross jurisdictional product.
  For example, a Hong Kong hedge fund would want to enforce HK rules
  on AML-KYC and regulatory compliance, and not be forced to enforce
  US or EU rules by technology.

* The business model of Polymath does not result on conflicts.
  Suppose I have a platform that is sponsored by VC fund A, and I want
  to use that technology to create a competing VC fund B, whose goal
  is to outcompete and put VC fund A out of business.  This is going
  to result in awkward situations.

# Trading infrastructure

One of the important aspects of the project is to create a trading
infrastructure that is independent from exchanges and to avoid
chokepoints.  We can create a p2p group and then find someone that can
do market making.


