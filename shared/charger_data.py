from __future__ import annotations

class Charger:
    class Status:
        NO_CAR = 0
        CHARGING = 1

    status: Status = Status.NO_CAR
    charge_percentage: float = 0.0 # [%] 0.0 - 100.0
    charging_rate: float = 0.0 # [%/s]
    
    def toggle_status(self):
        if self.status == Charger.Status.NO_CAR:
            self.status = Charger.Status.CHARGING
        else: self.status = Charger.Status.NO_CAR

class Location:
    def __init__(self, name: str):
        self.name: str = name
        self.chargers: list[Charger] = [Charger() for _ in range(5)]
