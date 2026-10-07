from abc import ABC, abstractmethod
from json import load, dump
from pathlib import Path
class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass
    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }   

class Reporter(BaseEntity):
    def __init__(self,id,name,email,team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError('Name cannot be empty')
        if '@' not in self.email:
            raise ValueError('Invalid email')


class Issue(BaseEntity):
    def __init__(self,id,title,description,reporter_id,status,priority):
        self.id = id
        self.title = title
        self.description = description
        self.reporter_id = reporter_id
        self.status = status
        self.priority = priority
        
    def validate(self):
        if not self.title:
            raise ValueError('Title cannot be empty')
        if not self.description:
            raise ValueError('Description cannot be empty')
        if not self.reporter_id:
            raise ValueError('Reporter id cannot be empty')
        if self.status not in ['open', 'in_progress', 'resolved','closed']:
            raise ValueError('Status has to be open, in_progress, resolved or closed')
        if self.priority not in ['low', 'medium', 'high','critical']:
            raise ValueError('Priority has to be low, medium, high or critical')

    def describe(self):
        return f"{self.title}  [{self.priority}]"

class CriticalIssue(Issue):
   
    def describe(self):
        return f"URGENT {self.title} - needs immediate attention"

class LowPriorityIssue(Issue):
   
    def describe(self):
        return f"{self.title} - low priority, handle when free"



    
