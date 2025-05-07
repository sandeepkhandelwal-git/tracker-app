from app.models.locations import UserLocation

def save_user_location(db, user_id: int, latitude: float, longitude: float):
    location = UserLocation(
                user_id = user_id,
                latitude = latitude,
                longitude = longitude
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location