# recommendation.py
from geopy.distance import geodesic 
import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import func
import json
from models import Monument, Event, MonumentEvent, DaySlot, MonumentSlot

def get_monuments_data(db: Session):
    """
    Fetch all monuments from the database with their related information
    """
    return db.query(Monument).all()

def get_events_data(db: Session):
    """
    Fetch all events from the database
    """
    return db.query(Event).all()

def monument_to_dict(monument):
    """Convert monument object to dictionary"""
    return {
        'id': monument.monument_id,
        'name': monument.name,
        'latitude': monument.latitude,
        'longitude': monument.longitude,
        'type': monument.type,
        'popularity': monument.popularity,
        'indoor': monument.indoor,
        'description': monument.description,
        'image_url': monument.image_url,
        'location': monument.location
    }

def get_monument_events(monument):
    """
    Get event names associated with a monument using the relationship
    """
    if hasattr(monument, 'monument_events') and monument.monument_events:
        return [me.event.name for me in monument.monument_events]
    return []

def get_monument_best_time(monument, db: Session):
    """
    Get the best time to visit a monument based on its slots
    """
    if hasattr(monument, 'slots') and monument.slots:
        slot_names = [slot.slot.slot_name for slot in monument.slots]
        # Find the most common time slot
        if slot_names:
            # print(max(set(slot_names), key=slot_names.count))
            return max(set(slot_names), key=slot_names.count)
    return None  # Default if no slots defined

def create_dataframes(db: Session):
    """
    Create DataFrames from database data for compatibility with existing code
    """
    monuments = get_monuments_data(db)
    events = get_events_data(db)
    
    # Process monument data
    monuments_data = []
    for monument in monuments:
        monument_dict = monument_to_dict(monument)
        
        # Add events
        monument_dict['events'] = get_monument_events(monument)
        
        # Add best time if available from day slots
        best_time = get_monument_best_time(monument, db)
        if best_time:
            monument_dict['best_time'] = best_time
        else:
            # Default based on type if no slot info
            if monument.type in ['Hindu Temple', 'Buddhist Stupa']:
                monument_dict['best_time'] = 'morning'
            elif monument.type in ['Museum', 'Historical Monument']:
                monument_dict['best_time'] = 'afternoon'
            else:
                monument_dict['best_time'] = 'afternoon'
        
        # Determine best season (simplified - could be expanded based on your needs)
        monument_dict['best_season'] = 'all'
        
        monuments_data.append(monument_dict)
    
    # Create DataFrames
    df = pd.DataFrame(monuments_data)
    
    # Process event data
    events_data = []
    for event in events:
        event_dict = {
            'name': event.name,
            'start_date': event.start_date.strftime('%Y-%m-%d') if event.start_date else None,
            'end_date': event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
            'related_type': event.related_type
        }
        events_data.append(event_dict)
    
    df_events = pd.DataFrame(events_data)
    
    return df, df_events

def norm_distance(curr_latitude, curr_longitude, df):
    """Calculate normalized distance from current location to monuments"""
    curr_point = (curr_latitude, curr_longitude)
    distance = np.zeros(len(df))
    max_distance = -1
    
    for i in range(len(df)):
        point = (df['latitude'].iloc[i], df['longitude'].iloc[i])
        distance[i] = geodesic(curr_point, point).km

        if max_distance < distance[i]:
            max_distance = distance[i]
    
    # Handle edge case where all monuments are at the same location
    if max_distance == 0:
        return np.ones(len(df))
        
    normalized_distance = (1 - distance/max_distance)
    return normalized_distance

def type_match(type_of_monument, df):
    """Score monuments based on matching monument type"""
    type_match_hotcoded = (type_of_monument == df['type']).astype(int)
    return np.array(type_match_hotcoded)

def single_event_score(event, current_date):
    """Score an event based on how close or current it is"""
    if not event.empty:
        s_d = event['start_date'].iloc[0]
        e_d = event['end_date'].iloc[0]
        
        if s_d and e_d:  # Check if dates are not None
            try:
                start_date = datetime.strptime(s_d, "%Y-%m-%d")
                end_date = datetime.strptime(e_d, "%Y-%m-%d")

                if current_date >= start_date and current_date <= end_date:
                    return 1
                elif current_date < start_date:
                    if abs((current_date - start_date)).days <= 7:
                        return 0.5
                    if abs((current_date - start_date)).days <= 14:
                        return 0.2
                    return 0
                else:
                    return 0
            except (ValueError, TypeError):
                return 0
    return 0
        
def calculate_date_score(current_date, df, df_events):
    """Calculate score for monuments based on upcoming or current events"""
    date_scores = np.zeros(len(df))

    for i in range(len(df)):
        max_score = 0
        events = df['events'].iloc[i]
        
        if events and isinstance(events, list):  # Check if events list is not empty
            for event in events:
                event_data = df_events[df_events['name'] == event]
                if not event_data.empty:
                    score = single_event_score(event_data, current_date)
                    if score > max_score:
                        max_score = score
                
            date_scores[i] = max_score

    return date_scores

def scores_time_of_day(current_hour, df):
    """Score monuments based on recommended visiting time"""
    # If best_time column doesn't exist, return zeros
    if 'best_time' not in df.columns:
        return np.zeros(len(df))
    
    # Initialize scores
    time_scores = np.zeros(len(df))
    
    # Morning: 6-12, Afternoon: 12-17, Evening: 17-21
    if 6 <= current_hour < 12:
        # Morning hours - higher score for morning attractions
        for i in range(len(df)):
            if df['best_time'].iloc[i] == 'morning':
                time_scores[i] = 1.0
            elif df['best_time'].iloc[i] == 'afternoon':
                time_scores[i] = 0.5
            else:
                time_scores[i] = 0.2
    elif 12 <= current_hour < 17:
        # Afternoon hours - higher score for afternoon attractions
        for i in range(len(df)):
            if df['best_time'].iloc[i] == 'afternoon':
                time_scores[i] = 1.0
            elif df['best_time'].iloc[i] in ['morning', 'evening']:
                time_scores[i] = 0.5
            else:
                time_scores[i] = 0.2
    else:
        # Evening hours - higher score for evening attractions
        for i in range(len(df)):
            if df['best_time'].iloc[i] == 'evening':
                time_scores[i] = 1.0
            elif df['best_time'].iloc[i] == 'afternoon':
                time_scores[i] = 0.7
            else:
                time_scores[i] = 0.3

    return time_scores

def final_weight_sum(user, df, df_events):
    """Calculate final recommendation weights for all monuments"""
    # Calculate individual factors
    distance = norm_distance(user['latitude'], user['longitude'], df)
    type_matched = type_match(user['likes'], df)
    popularity = np.array(df['popularity'])
    seasonal_event = calculate_date_score(datetime.now(), df, df_events)
    time_of_day = scores_time_of_day(datetime.now().hour, df)

    # Combine factors with weights
    total = 0.4 * distance + 0.2 * type_matched + 0.15 * popularity + 0.2 * seasonal_event + 0.05 * time_of_day

    return total

def recommend_monuments(user_lat=27.7104, user_long=85.3487, preferred_type="Hindu Temple"):
    """
    Main function to recommend monuments based on user preferences.
    Returns a sorted list of monument objects.
    
    Parameters:
    - user_lat: float - user's latitude
    - user_long: float - user's longitude
    - preferred_type: str - type of monument the user prefers
    
    Returns:
    - List of monument objects sorted by recommendation score
    """
    # User preferences
    user = {
        'latitude': user_lat,
        'longitude': user_long,
        'likes': preferred_type,
        'current_time': datetime.now().hour,
        'current_date': datetime.now()
    }
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create dataframes from database data
        df, df_events = create_dataframes(db)
        
        # Check if dataframes are empty
        if df.empty:
            return []
        
        # Calculate weights and recommendations
        final_weights = final_weight_sum(user, df, df_events)
        
        # Create a list of monuments with their weights
        monuments_with_weights = []
        for i in range(len(df)):
            monument = {
                'id': int(df['id'].iloc[i]),
                'name': df['name'].iloc[i],
                'latitude': float(df['latitude'].iloc[i]),
                'longitude': float(df['longitude'].iloc[i]),
                'type': df['type'].iloc[i],
                'popularity': float(df['popularity'].iloc[i]),
                'indoor': bool(df['indoor'].iloc[i]),
                'description': df['description'].iloc[i],
                'image_url': df['image_url'].iloc[i],
                'location': df['location'].iloc[i],
                'weight': float(final_weights[i])  # Add the calculated weight
            }
            monuments_with_weights.append(monument)
        
        # Sort monuments by weight in descending order
        sorted_monuments = sorted(monuments_with_weights, key=lambda x: x['weight'], reverse=True)
        
        # Remove the weight field from the final response
        for monument in sorted_monuments:
            del monument['weight']
        
        return sorted_monuments
    except Exception as e:
        print(f"Error in recommendation: {str(e)}")
        return []
    finally:
        db.close()