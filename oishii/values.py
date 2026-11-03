from enum import Enum

class AgentType(Enum):
    CONCIERGE = 'concierge_guide'
    NUTRITIONIST = 'nutritionist_feedback'

class MenuStatus(Enum):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'
    ERROR = 'error'

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'