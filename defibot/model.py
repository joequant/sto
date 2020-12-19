from ariadne import QueryType
from defibotlocal import DefibotLocal

dfbl = DefibotLocal()
query = QueryType()
@query.field("hello")
def resolve_hello(_, info):
    return "Hi there"

@query.field("testpending")
def test_pending(_, info):
    return dfbl.test_pending()

@query.field("testuniswap")
def test_pending(_, info):
    return dfbl.test_uniswap()
