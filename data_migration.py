from database import SessionLocal
from models import Monument, Tag, Event, MonumentEvent, DaySlot, MonumentSlot
from recommendation import monuments_data, events_data
from datetime import datetime

def migrate_data():
    db = SessionLocal()
    
    # Create tags
    tag_map = {}
    for monument in monuments_data:
        monument_type = monument.get("type")
        if monument_type and not db.query(Tag).filter(Tag.tag_name == monument_type).first():
            tag = Tag(tag_name=monument_type)
            db.add(tag)
            db.commit()
            db.refresh(tag)
            tag_map[monument_type] = tag
    
    # Add monuments with tags
    monument_map = {}
    for monument_data in monuments_data:
        monument = Monument(
            name=monument_data["name"],
            latitude=monument_data["latitude"],
            longitude=monument_data["longitude"],
            popularity=monument_data["popularity"],
            indoor=monument_data["indoor"],
        )
        
        # Link tags
        monument_type = monument_data.get("type")
        if monument_type and monument_type in tag_map:
            monument.tags.append(tag_map[monument_type])
            
        db.add(monument)
        db.commit()
        db.refresh(monument)
        
        # Store monument for linking events later
        monument_map[monument_data["name"]] = monument
    
    # Add events
    event_map = {}
    for event_data in events_data:
        event = Event(
            name=event_data["name"],
            start_date=datetime.strptime(event_data["start_date"], "%Y-%m-%d"),
            end_date=datetime.strptime(event_data["end_date"], "%Y-%m-%d"),
            related_type=event_data["related_type"]
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        event_map[event_data["name"]] = event
    
    # Link monuments and events
    for monument_data in monuments_data:
        monument = monument_map.get(monument_data["name"])
        if monument and "events" in monument_data:
            for event_name in monument_data["events"]:
                event = event_map.get(event_name)
                if event:
                    # Check if relationship already exists
                    existing = db.query(MonumentEvent).filter(
                        MonumentEvent.monument_id == monument.monument_id,
                        MonumentEvent.event_id == event.event_id
                    ).first()
                    
                    if not existing:
                        monument_event = MonumentEvent(
                            monument_id=monument.monument_id,
                            event_id=event.event_id,
                            name=event_name
                        )
                        db.add(monument_event)
    
    # Add time slots (morning, afternoon, evening)
    time_slots = ["morning", "afternoon", "evening"]
    for slot_name in time_slots:
        if not db.query(DaySlot).filter_by(slot_name=slot_name).first():
            slot = DaySlot(slot_name=slot_name)
            db.add(slot)
    
    db.commit()
    
    # Link monuments to their best time slots
    slots = {slot.slot_name: slot for slot in db.query(DaySlot).all()}
    for monument_data in monuments_data:
        if "best_time" in monument_data:
            best_time = monument_data["best_time"]
            monument = monument_map.get(monument_data["name"])
            slot = slots.get(best_time)
            
            if monument and slot:
                monument_slot = MonumentSlot(
                    monument_id=monument.monument_id,
                    slot_id=slot.slot_id
                )
                db.add(monument_slot)
    
    db.commit()
    db.close()
    
    print("Data migration completed successfully!")

if __name__ == "__main__":
    migrate_data()