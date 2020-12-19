from ariadne import QueryType
from defibot import DefibotLocal

dfbl = DefibotLocal()
query = QueryType()
@query.field("hello")
def resolve_hello(_, info):
    return "Hi there"

