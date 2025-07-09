from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel, Field
from pydantic_ai.agent import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider


class Foo(BaseModel):
    positive: int = Field(gt=0)
    non_negative: int = Field(ge=0)
    negative: int = Field(lt=0)
    non_positive: int = Field(le=0)
    even: int = Field(multiple_of=2)
    love_for_pydantic: float = Field(allow_inf_nan=True)
    short: str = Field(min_length=3)
    long: str = Field(max_length=10)
    regex: str = Field(pattern=r'^\d*$') 
    precise: Decimal = Field(max_digits=5, decimal_places=2)

foo = Foo(
    positive=1,
    non_negative=0,
    negative=-1,
    non_positive=0,
    even=18,
    love_for_pydantic=float('inf'),
    short='foo',
    long='foobarbaz',
    regex='123',
)
print(foo)