from typing import List, Dict, Any  # Type hints for lists, dictionaries, and any type of data
from langchain_core.output_parsers import PydanticOutputParser  # Output parser for Pydantic models
from pydantic import BaseModel, Field  # Base model and field for data validation and default values


# Define a Pydantic model to structure and validate LinkedIn profile summaries
class Summary(BaseModel):
    # A short text summary describing the individual
    summary: str = Field(description="Summary of the individual")

    # A list of interesting facts about the individual
    facts: List[str] = Field(default_factory=list, description="Interesting facts about the individual")

    # A list of icebreakers related to the individual, useful for conversation starters
    ice_breakers: List[str] = Field(default_factory=list, description="Ice breakers related to the individual")

    # A list of topics of interest related to the individual
    topics_of_interest: List[str] = Field(default_factory=list,
                                          description="Topics of interest related to the individual")

    # Method to convert the Pydantic model instance into a dictionary format
    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts,
            "ice_breakers": self.ice_breakers,
            "topics_of_interest": self.topics_of_interest
        }


# Instantiate a parser to parse model output into a structured Summary object
summary_parser = PydanticOutputParser(pydantic_object=Summary)
