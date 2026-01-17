import os
from pymongo.server_api import ServerApi
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import motor.motor_asyncio
import io
from bson import ObjectId
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Connect to MongoDB Atlas
uri = os.getenv('MONGO_URI')
client = motor.motor_asyncio.AsyncIOMotorClient(uri, server_api=ServerApi('1'), tls=True)
db = client.event_management_db

# Test MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI')

def test_mongo_connection():
    try:
        # Try with SSL disabled for testing (not recommended for production)
        client = MongoClient(MONGO_URI, ssl=False)
        client.admin.command('ping')  # This will ping the server
        print("MongoDB connection successful (SSL disabled)!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

test_mongo_connection()

# Data Models
class Event(BaseModel):
    venue_id: str
    event_title: str
    event_biography: str
    event_date: str
    event_time: str

class Attendee(BaseModel):
    attendee_name: str
    attendee_surname: str
    attendee_email: str
    phone: Optional[str] = None

class Venue(BaseModel):
    venue_name: str
    venue_address: str
    capacity: int

class Booking(BaseModel):
    event_id: str
    attendee_id: str
    booking_date: str
    booking_status: str

# Event Endpoints

# Creates a Event to the database
@app.post("/events")
async def create_event(event: Event):
    """
    Creates a new event in the database with the provided event details.
    """
    event_doc = event.dict()
    result = await db.events.insert_one(event_doc)
    return {"message": "Event created", "id": str(result.inserted_id)}

# Retrieves all Events from the database
@app.get("/events")
async def get_events():
    """
    Retrieves all events from the database.
    """
    events = await db.events.find().to_list(100)
    for event in events:
        event["_id"] = str(event["_id"])
    return events

# Retrieves a specific Event by ID
@app.get("/events/{event_id}")
async def get_event(event_id: str):
    """
    Retrieves a specific event by its ID from the database.
    """
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    if event:
        event["_id"] = str(event["_id"])
        return event
    raise HTTPException(status_code=404, detail="Event not found")

# Updates a specific Event by ID
@app.put("/events/{event_id}")
async def update_event(event_id: str, event: Event):
    """
    Updates a specific event by its ID with new event details.
    """
    update_data = event.dict()
    result = await db.events.update_one({"_id": ObjectId(event_id)}, {"$set": update_data})
    if result.modified_count == 1:
        return {"message": "Event updated"}
    raise HTTPException(status_code=404, detail="Event not found")

# Deletes a specific Event by ID
@app.delete("/events/{event_id}")
async def delete_event(event_id: str):
    """
    Deletes a specific event by its ID from the database.
    """
    result = await db.events.delete_one({"_id": ObjectId(event_id)})
    if result.deleted_count == 1:
        return {"message": "Event deleted"}
    raise HTTPException(status_code=404, detail="Event not found")

# Attendee Endpoints

# Creates an Attendee to the database
@app.post("/attendees")
async def create_attendee(attendee: Attendee):
    """
    Creates a new attendee in the database with the provided attendee details.
    """
    attendee_doc = attendee.dict()
    result = await db.attendees.insert_one(attendee_doc)
    return {"message": "Attendee created", "id": str(result.inserted_id)}

# Retrieves all Attendees from the database
@app.get("/attendees")
async def get_attendees():
    """
    Retrieves all attendees from the database.
    """
    attendees = await db.attendees.find().to_list(100)
    for attendee in attendees:
        attendee["_id"] = str(attendee["_id"])
    return attendees

# Retrieves a specific Attendee by ID
@app.get("/attendees/{attendee_id}")
async def get_attendee(attendee_id: str):
    """
    Retrieves a specific attendee by their ID from the database.
    """
    attendee = await db.attendees.find_one({"_id": ObjectId(attendee_id)})
    if attendee:
        attendee["_id"] = str(attendee["_id"])
        return attendee
    raise HTTPException(status_code=404, detail="Attendee not found")

# Updates a specific Attendee by ID
@app.put("/attendees/{attendee_id}")
async def update_attendee(attendee_id: str, attendee: Attendee):
    """
    Updates a specific attendee by their ID with new attendee details.
    """
    update_data = attendee.dict()
    result = await db.attendees.update_one({"_id": ObjectId(attendee_id)}, {"$set": update_data})
    if result.modified_count == 1:
        return {"message": "Attendee updated"}
    raise HTTPException(status_code=404, detail="Attendee not found")

# Deletes a specific Attendee by ID
@app.delete("/attendees/{attendee_id}")
async def delete_attendee(attendee_id: str):
    """
    Deletes a specific attendee by their ID from the database.
    """
    result = await db.attendees.delete_one({"_id": ObjectId(attendee_id)})
    if result.deleted_count == 1:
        return {"message": "Attendee deleted"}
    raise HTTPException(status_code=404, detail="Attendee not found")

# Venue Endpoints

# Creates a Venue to the database
@app.post("/venues")
async def create_venue(venue: Venue):
    """
    Creates a new venue in the database with the provided venue details.
    """
    venue_doc = venue.dict()
    result = await db.venues.insert_one(venue_doc)
    return {"message": "Venue created", "id": str(result.inserted_id)}


# Retrieves all Venues from the database
@app.get("/venues")
async def get_venues():
    """
    Retrieves all venues from the database.
    """
    venues = await db.venues.find().to_list(100)
    for venue in venues:
        venue["_id"] = str(venue["_id"])
    return venues

# Retrieves a specific Venue by ID
@app.get("/venues/{venue_id}")
async def get_venue(venue_id: str):
    """
    Retrieves a specific venue by its ID from the database.
    """
    from bson import ObjectId
    venue = await db.venues.find_one({"_id": ObjectId(venue_id)})
    if venue:
        venue["_id"] = str(venue["_id"])
        return venue
    raise HTTPException(status_code=404, detail="Venue not found")

# Updates a specific Venue by ID
@app.put("/venues/{venue_id}")
async def update_venue(venue_id: str, venue: Venue):
    """
    Updates a specific venue by its ID with new venue details.
    """
    from bson import ObjectId
    update_data = venue.dict()
    result = await db.venues.update_one({"_id": ObjectId(venue_id)}, {"$set": update_data})
    if result.modified_count == 1:
        return {"message": "Venue updated"}
    raise HTTPException(status_code=404, detail="Venue not found")

# Deletes a specific Venue by ID
@app.delete("/venues/{venue_id}")
async def delete_venue(venue_id: str):
    """
    Deletes a specific venue by its ID from the database.
    """
    result = await db.venues.delete_one({"_id": ObjectId(venue_id)})
    if result.deleted_count == 1:
        return {"message": "Venue deleted"}
    raise HTTPException(status_code=404, detail="Venue not found")

# Booking Endpoints

# Creates a Booking to the database
@app.post("/bookings")
async def create_booking(booking: Booking):
    """
    Creates a new booking in the database with the provided booking details.
    """
    booking_doc = booking.dict()
    result = await db.bookings.insert_one(booking_doc)
    return {"message": "Booking created", "id": str(result.inserted_id)}

# Retrieves all Bookings from the database
@app.get("/bookings")
async def get_bookings():
    """
    Retrieves all bookings from the database.
    """
    bookings = await db.bookings.find().to_list(100)
    for booking in bookings:
        booking["_id"] = str(booking["_id"])
    return bookings

# Retrieves a specific Booking by ID
@app.get("/bookings/{booking_id}")
async def get_booking(booking_id: str):
    """
    Retrieves a specific booking by its ID from the database.
    """
    from bson import ObjectId
    booking = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    if booking:
        booking["_id"] = str(booking["_id"])
        return booking
    raise HTTPException(status_code=404, detail="Booking not found")

# Updates a specific Booking by ID
@app.put("/bookings/{booking_id}")
async def update_booking(booking_id: str, booking: Booking):
    """
    Updates a specific booking by its ID with new booking details.
    """
    update_data = booking.dict()
    result = await db.bookings.update_one({"_id": ObjectId(booking_id)}, {"$set": update_data})
    if result.modified_count == 1:
        return {"message": "Booking updated"}
    raise HTTPException(status_code=404, detail="Booking not found")

@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: str):
    """
    Deletes a specific booking by its ID from the database.
    """
    result = await db.bookings.delete_one({"_id": ObjectId(booking_id)})
    if result.deleted_count == 1:
        return {"message": "Booking deleted"}
    raise HTTPException(status_code=404, detail="Booking not found")

# Upload Event Poster (Image)

# Upload Event Poster
@app.post("/upload_event_poster/{event_id}")
async def upload_event_poster(event_id: str, file: UploadFile = File(...)):
    """
    Uploads an event poster image for a specific event and stores it in the database.
    """
    content = await file.read()
    poster_doc = {
    "event_id": event_id,
    "filename": file.filename,
    "content_type": file.content_type,
    "content": content,
    "uploaded_at": datetime.utcnow()
}
    result = await db.event_posters.insert_one(poster_doc)
    return {"message": "Event poster uploaded", "id": str(result.inserted_id)}

# Get Event Poster
@app.get("/event_poster/{poster_id}")
async def get_event_poster(poster_id: str):
    """
    Retrieves and streams an event poster image by its ID from the database.
    """
    poster = await db.event_posters.find_one({"_id": ObjectId(poster_id)})
    if poster:
        return StreamingResponse(io.BytesIO(poster["content"]), media_type=poster["content_type"])
    raise HTTPException(status_code=404, detail="Poster not found")

# Upload Promotional Video
@app.post("/upload_promotional_video/{event_id}")
async def upload_promotional_video(event_id: str, file: UploadFile = File(...)):
    """
    Uploads a promotional video for a specific event and stores it in the database.
    """
    content = await file.read()
    video_doc = {
    "event_id": event_id,
    "filename": file.filename,
    "content_type": file.content_type,
    "content": content,
    "uploaded_at": datetime.utcnow()
}
    result = await db.promotional_videos.insert_one(video_doc)
    return {"message": "Promotional video uploaded", "id": str(result.inserted_id)}

# Get Promotional Video
@app.get("/promotional_video/{video_id}")
async def get_promotional_video(video_id: str):
    """
    Retrieves and streams a promotional video by its ID from the database.
    """
    video = await db.promotional_videos.find_one({"_id": ObjectId(video_id)})
    if video:
        return StreamingResponse(io.BytesIO(video["content"]), media_type=video["content_type"])
    raise HTTPException(status_code=404, detail="Video not found")

# Upload Venue Photo
@app.post("/upload_venue_photo/{venue_id}")
async def upload_venue_photo(venue_id: str, file: UploadFile = File(...)):
    """
    Uploads a photo for a specific venue and stores it in the database.
    """
    content = await file.read()
    photo_doc = {
    "venue_id": venue_id,
    "filename": file.filename,
    "content_type": file.content_type,
    "content": content,
    "uploaded_at": datetime.utcnow()
}
    result = await db.venue_photos.insert_one(photo_doc)
    return {"message": "Venue photo uploaded", "id": str(result.inserted_id)}

# Get Venue Photo
@app.get("/venue_photo/{photo_id}")
async def get_venue_photo(photo_id: str):
    """
    Retrieves and streams a venue photo by its ID from the database.
    """
    photo = await db.venue_photos.find_one({"_id": ObjectId(photo_id)})
    if photo:
        return StreamingResponse(io.BytesIO(photo["content"]), media_type=photo["content_type"])
    raise HTTPException(status_code=404, detail="Photo not found")

if __name__ == "__main__":
    test_mongo_connection()