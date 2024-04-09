from __future__ import annotations

class Charger:
    class Status:
        NO_CAR = 0
        CHARGING = 1

    status: Status = Status.NO_CAR
    charge_percentage: float = 0.0 # [%] 0.0 - 100.0
    charging_rate: float = 0.0 # [%/s]

class Location:
    name: str
    chargers: list[Charger]
