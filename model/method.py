from dataclasses import dataclass


@dataclass
class Method():
    Order_method_code: int
    Order_method_type: str

    def __hash__(self):
        return hash(self.Order_method_code)
