from datetime import date
from pydantic import BaseModel, Field
from streamlit_card import card


class Player(BaseModel):
    name: str
    color: str
    facts: list[str] = Field(default_factory=list)

    def card(self):
        return card(title=self.name, text=self.facts)
