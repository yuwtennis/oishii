from pydantic import BaseModel, Field
from typing import Literal, List

class UserDemographic(BaseModel):
    age: int = Field(
        description='Age of the user',
        default=40,
    )
    gender: Literal['male', 'female'] = Field(
        description='Gender of the user',
        default='male',
    )

class Feedback(BaseModel):
    status: Literal['healthy', 'unhealthy'] = Field(
        description='Whether the dish is healthy or not',
    )
    restaurant_name: str = Field(
        description='Name of the restaurant',
    )
    menu_name: str = Field(
        description='Name of the menu item',
    )
    feedback: str = Field(
        description='Detailed feedbacks from the nutritionist. If healthy, brief expression why the dish is healthy.',
    )

class NutritionistFeedback(BaseModel):
    feedbacks: List[Feedback] = Field(
        description='List of feedbacks from the nutritionist',
    )
