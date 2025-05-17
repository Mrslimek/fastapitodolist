from enum import Enum


class TaskStatus(Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    
def get_enum_values(enum_class: Enum):
    return [member.value for member in enum_class]