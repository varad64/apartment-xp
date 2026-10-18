from model import Flat, ServantRoom

def create_flats() -> list[Flat]:
    return [
        Flat(flat_number="001", area=2471, family_name="Patil"),
        Flat(flat_number="002", area=2239, family_name="Deshpande", servant_room=ServantRoom(room_number="003", area=142, assigned_to_flat="002")),
        Flat(flat_number="101", area=3071, family_name="Kulkarni"),
        Flat(flat_number="102", area=2300, family_name="Seth", servant_room=ServantRoom(room_number="103", area=142, assigned_to_flat="102")),
        Flat(flat_number="201", area=3071, family_name="Raina", servant_room=ServantRoom(room_number="203", area=142, assigned_to_flat="201")),
        Flat(flat_number="202", area=2300, family_name="Deshpande"),
        Flat(flat_number="301", area=3071, family_name="Dhoni"),
        Flat(flat_number="302", area=2300, family_name="Bhat", servant_room=ServantRoom(room_number="303", area=142, assigned_to_flat="302")),
        Flat(flat_number="401", area=3638, family_name="Sharma", servant_room=ServantRoom(room_number="403", area=142, assigned_to_flat="401")),
        Flat(flat_number="402", area=2811, family_name="Sehwag"),
    ]