class Availability:
    class Current:
        available_chargers = 0
    class OnArrival:
        available_chargers = 0
    #class Future:
    
    current = Current()
    on_arrival = OnArrival()
    
    time_until_arrival: int = 0 #[minutes]
    total_chargers = 0