from __future__ import annotations
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_graph import BaseNode, GraphRunContext, End, Graph
from dataclasses import dataclass
from IPython.display import Image, display


@dataclass
class DivisibleBy5(BaseNode[None, None, int]):  
    foo: int

    async def run(
        self,
        ctx: GraphRunContext,
    ) -> Increment | End[int]:
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return Increment(self.foo)

@dataclass
class Increment(BaseNode):  
    foo: int

    async def run(self, ctx: GraphRunContext) -> DivisibleBy5:
        return DivisibleBy5(self.foo + 1)



fives_graph = Graph(nodes=[DivisibleBy5, Increment])  
result = fives_graph.run_sync(DivisibleBy5(26))  
print(result.output)

display(Image(fives_graph.mermaid_image(start_node=DivisibleBy5(26))))
