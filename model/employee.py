import datetime
from dataclasses import dataclass

@dataclass
class Employee:
    EmployeeId: int
    LastName: str
    FirstName: str
    Title: str
    ReportsTo: int
    BirthDate: datetime.time
    HireDate: datetime.time
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str

    def __hash__(self):
        return hash(self.EmployeeId)

    def __eq__(self, other):
        return self.EmployeeId == other.EmployeeId

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"