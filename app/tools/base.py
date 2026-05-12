from abc import ABC, abstractmethod
from langchain_core.tools import StructuredTool


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def function(self, **kwargs):
        ...

    def to_langchain_tool(self) -> StructuredTool:
        return StructuredTool.from_function(
            func=self.function,
            name=self.name,
            description=self.description,
        )
