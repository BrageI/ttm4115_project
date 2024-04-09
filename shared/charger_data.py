from __future__ import annotations

class Charger:
    class Status:
        NO_CAR = 0
        CHARGING = 1

    status: Status = Status.NO_CAR
    charger_number: int 
    charge_percentage: float = 0.0 # [%] 0.0 - 100.0
    charging_rate: float = 0.0 # [%/s]
    
    def __init__(self, number):
        self.charger_number = number
    
    def toggle_status(self):
        if self.status == Charger.Status.NO_CAR:
            self.status = Charger.Status.CHARGING
        else: self.status = Charger.Status.NO_CAR

class Location:
    def __init__(self, name: str):
        self.name: str = name
        self.chargers: list[Charger] = [Charger(i) for i in range(5)]
