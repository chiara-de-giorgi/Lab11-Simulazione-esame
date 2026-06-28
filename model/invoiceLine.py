from dataclasses import dataclass
@dataclass
class InvoiceLine:
    InvoiceLineId: int
    InvoiceId: int
    TrackId: int
    UnitPrice: float
    Quantity: int

    def __hash__(self):
        return hash(self.InvoiceId)

    def __eq__(self, other):
        return self.InvoiceId == other.InvoiceId

    def __str__(self):
        pass