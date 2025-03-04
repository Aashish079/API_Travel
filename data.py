# Backend now uses data from database, these are kehp here just for populating database if needed again

monuments_data = [
  {
    "id": 1,
    "name": "Pashupatinath Temple",
    "latitude": 27.7104,
    "longitude": 85.3487,
    "location": "Kathmandu, Nepal",
    "type": "Hindu Temple",
    "popularity": 0.95,
    "indoor": False,
    "best_season": "all",
    "best_time": "morning",
    "events": [
      "Maha Shivaratri",
      "Tihar Festival"
    ],
    "description": "Ancient Hindu temple dedicated to Lord Shiva located on the banks of the Bagmati River.",
    "image_url": "/assets/Pashupatinath_Temple.jpg"
  },
  {
    "id": 2,
    "name": "Boudhanath Stupa",
    "latitude": 27.7139,
    "longitude": 85.36,
    "location": "Kathmandu, Nepal",
    "type": "Buddhist Stupa",
    "popularity": 0.92,
    "indoor": False,
    "best_season": "spring",
    "best_time": "morning",
    "events": [
      "Buddha Jayanti"
    ],
    "description": "One of the largest spherical stupas in Nepal and the holiest Tibetan Buddhist temple outside Tibet.",
    "image_url": "/assets/Boudhanath_Stupa.jpg"
  },
  {
    "id": 3,
    "name": "Swayambhunath Stupa",
    "latitude": 27.7149,
    "longitude": 85.2904,
    "location": "Kathmandu, Nepal",
    "type": "Buddhist Stupa",
    "popularity": 0.88,
    "indoor": False,
    "best_season": "all",
    "best_time": "morning",
    "events": [
      "Tihar Festival",
      "Buddha Jayanti"
    ],
    "description": "Ancient religious architecture atop a hill in the Kathmandu Valley, nicknamed 'Monkey Temple'.",
    "image_url": "/assets/Swayambhunath_Stupa.jpg"
  },
  {
    "id": 4,
    "name": "Durbar Square",
    "latitude": 27.7101,
    "longitude": 85.3,
    "location": "Kathmandu, Nepal",
    "type": "Historical Monument",
    "popularity": 0.85,
    "indoor": False,
    "best_season": "autumn",
    "best_time": "afternoon",
    "events": [
      "New Year Celebration"
    ],
    "description": "Popular plaza in front of the old royal palace featuring traditional Newari architecture.",
    "image_url": "/assets/Durbar_Square.jpg"
  },
  {
    "id": 5,
    "name": "Patan Durbar Square",
    "latitude": 27.671,
    "longitude": 85.3245,
    "location": "Lalitpur, Nepal",
    "type": "Historical Monument",
    "popularity": 0.9,
    "indoor": False,
    "best_season": "autumn", 
    "best_time": "afternoon",
    "events": [
      "Holi Festival",
      "Bisket Jatra"  
    ],
    "description": "One of the three Durbar Squares in the Kathmandu Valley, located in the city of Lalitpur.",
    "image_url": "/assets/Patan_Durbar_Square.jpg"
  },
  {
    "id": 6,
    "name": "Bhaktapur Durbar Square",
    "latitude": 27.6749,
    "longitude": 85.429,
    "location": "Bhaktapur, Nepal",
    "type": "Historical Monument",
    "popularity": 0.87,
    "indoor": False,
    "best_season": "spring",
    "best_time": "morning",
    "events": [
      "Bisket Jatra"
    ],
    "description": "Former royal palace complex showcasing 15th-century Newari architecture and temples.",
    "image_url": "/assets/Bhaktapur_Durbar_Square.jpg"
  },
  {
    "id": 7,
    "name": "Garden of Dreams",
    "latitude": 27.717,
    "longitude": 85.292,
    "location": "Kathmandu, Nepal",
    "type": "Garden",
    "popularity": 0.75,
    "indoor": False,
    "best_season": "all",
    "best_time": "afternoon",
    "events": [
      "Christmas Celebration"
    ],
    "description": "Neo-classical historical garden featuring fountains, pavilions, and amphitheaters.",
    "image_url": "/assets/Garden_of_Dreams.jpg"
  },
  {
    "id": 9,
    "name": "Kumari Ghar",
    "latitude": 27.7111,
    "longitude": 85.2964,
    "location": "Kathmandu, Nepal",
    "type": "Palace",
    "popularity": 0.79,
    "indoor": True,
    "best_season": "winter",
    "best_time": "morning",
    "events": [
      "Dashain Festival",
      "Tihar Festival"
    ],
    "description": "A three-story brick building that is home to Nepal's living goddess, the Kumari.",
    "image_url": "/assets/Kumari_Ghar.jpg"
  },
  {
    "id": 10,
    "name": "Rani Pokhari",
    "latitude": 27.71,
    "longitude": 85.293,
    "location": "Kathmandu, Nepal", 
    "type": "Historical Site",
    "popularity": 0.7,
    "indoor": False,
    "best_season": "summer",
    "best_time": "afternoon",
    "events": [
      "Nepal Sambat New Year"
    ],
    "description": "Historical artificial pond featuring a temple in the center, located near Durbar Square.",
    "image_url": "/assets/Rani_Pokhari.jpg"
  },
  {
    "id": 11,
    "name": "Changu Narayan Temple",
    "latitude": 27.6749,
    "longitude": 85.4316,
    "location": "Bhaktapur, Nepal",
    "type": "Hindu Temple",
    "popularity": 0.72,
    "indoor": False,
    "best_season": "all",
    "best_time": "morning",
    "events": [
      "Maha Shivaratri",
      "Tihar Festival"
    ],
    "description": "Ancient Hindu temple from the 4th century dedicated to Lord Vishnu.",
    "image_url": "/assets/Changu_Narayan_Temple.jpg"
  },
  {
    "id": 12,
    "name": "Lalitpur (Patan) Museum",
    "latitude": 27.6699,
    "longitude": 85.325,
    "location": "Lalitpur, Nepal",
    "type": "Museum",
    "popularity": 0.77,
    "indoor": True,
    "best_season": "all",
    "best_time": "afternoon",
    "events": [
      "Art Exhibition"
    ],
    "description": "Museum featuring collections of historical and ancient artworks from Nepal.",
    "image_url": "/assets/Lalitpur_Patan_Museum.jpg"
  },
  {
    "id": 13,
    "name": "The National Museum",
    "latitude": 27.7041,
    "longitude": 85.2899,
    "location": "Kathmandu, Nepal",
    "type": "Museum",
    "popularity": 0.8,
    "indoor": True,
    "best_season": "all",
    "best_time": "morning",
    "events": [
      "National Holiday Celebration"
    ],
    "description": "Nepal's largest museum, showcasing its history, art, and culture.",
    "image_url": "/assets/The_National_Museum.jpg"
  },
  {
    "id": 14,
    "name": "Gosaikunda Temple",
    "latitude": 28.197,
    "longitude": 85.4486,
    "location": "Langtang National Park, Nepal",
    "type": "Hindu Temple",
    "popularity": 0.85,
    "indoor": False,
    "best_season": "winter",
    "best_time": "morning",
    "events": [
      "Janai Purnima Festival"
    ],
    "description": "Hindu temple located at high altitude surrounding Gosaikunda lakes.",
    "image_url": "/assets/Gosaikunda_Temple.jpg"
  },
  {
    "id": 15,
    "name": "Sundhara",
    "latitude": 27.7009,
    "longitude": 85.3033,
    "location": "Kathmandu, Nepal",
    "type": "Historical Site",
    "popularity": 0.68,
    "indoor": False,
    "best_season": "summer",
    "best_time": "afternoon",
    "events": [
      "Independence Day"  
    ],
    "description": "Medieval stone spout and important historical site in Kathmandu.", 
    "image_url": "/assets/Sundhara.jpg"
  },
  {
    "id": 16,
    "name": "Taleju Temple",
    "latitude": 27.7108,
    "longitude": 85.298,
    "location": "Kathmandu, Nepal",
    "type": "Hindu Temple", 
    "popularity": 0.9,
    "indoor": False,
    "best_season": "all",
    "best_time": "morning",
    "events": [
      "Dashain Festival",
      "Tihar Festival"
    ],
    "description": "Important Hindu temple located in the old royal palace complex of Kathmandu.",
    "image_url": "/assets/Taleju_Temple.jpg"
  },
  {
    "id": 17,
    "name": "Maha Laxmi Temple",
    "latitude": 27.71, 
    "longitude": 85.3005,
    "location": "Kathmandu, Nepal",
    "type": "Hindu Temple",
    "popularity": 0.88,
    "indoor": False,
    "best_season": "all",
    "best_time": "morning",
    "events": [
      "Tihar Festival"
    ],
    "description": "Hindu temple dedicated to goddess of wealth and fortune Lakshmi.",
    "image_url": "/assets/Maha_Laxmi_Temple.jpg" 
  },
  {
    "id": 18,
    "name": "Narayanhiti Palace Museum",
    "latitude": 27.7124,
    "longitude": 85.3201,
    "location": "Kathmandu, Nepal",  
    "type": "Museum",
    "popularity": 0.84,
    "indoor": True,
    "best_season": "spring",
    "best_time": "afternoon", 
    "events": [
      "Republic Day"
    ],
    "description": "Former royal palace converted into a museum showcasing artifacts from Nepal's monarchy.",
    "image_url": "/assets/Narayanhiti_Palace_Museum.jpg"
  },
  {
    "id": 19,
    "name": "Bikram Sambat Park",
    "latitude": 27.7012,
    "longitude": 85.2873,
    "location": "Kathmandu, Nepal", 
    "type": "Park",
    "popularity": 0.71,
    "indoor": False,
    "best_season": "spring",
    "best_time": "morning",
    "events": [
      "Bikram Sambat New Year" 
    ],
    "description": "Public park named after Nepal's Bikram Sambat calendar.",
    "image_url": "/assets/Bikram_Sambat_Park.jpg"
  },
  {
    "id": 20,
    "name": "Chobhar Caves",
    "latitude": 27.6267,
    "longitude": 85.325,
    "location": "Kathmandu Valley, Nepal",
    "type": "Cave",
    "popularity": 0.65,
    "indoor": True,
    "best_season": "autumn", 
    "best_time": "afternoon",
    "events": [
      "Autumn Festival"
    ],
    "description": "Natural limestone caves located in the southern part of Kathmandu Valley.",
    "image_url": "/assets/Chobhar_Caves.jpg"
  }
]

events_data = [
    {"name": "Dashain Festival", "start_date": "2025-10-10", "end_date": "2025-10-24", "related_type": "Hindu Temples"},
    {"name": "Buddha Jayanti", "start_date": "2025-05-15", "end_date": "2025-05-20", "related_type": "Buddhist Temples"},
    {"name": "Tihar Festival", "start_date": "2025-11-01", "end_date": "2025-11-05", "related_type": "Hindu Temples"},
    {"name": "Maha Shivaratri", "start_date": "2025-02-25", "end_date": "2025-02-26", "related_type": "Hindu Temples"},
    {"name": "New Year Celebration", "start_date": "2025-01-01", "end_date": "2025-01-01", "related_type": "Historical Monuments"},
    {"name": "Holi Festival", "start_date": "2025-03-10", "end_date": "2025-03-11", "related_type": "Historical Monuments"},
    {"name": "Bisket Jatra", "start_date": "2025-04-10", "end_date": "2025-04-18", "related_type": "Historical Monuments"},
    {"name": "Christmas Celebration", "start_date": "2025-12-25", "end_date": "2025-12-25", "related_type": "Gardens"},
    {"name": "Nepal Sambat New Year", "start_date": "2025-11-05", "end_date": "2025-11-05", "related_type": "Historical Sites"},
    {"name": "Art Exhibition", "start_date": "2025-07-01", "end_date": "2025-07-10", "related_type": "Museums"},
    {"name": "National Holiday Celebration", "start_date": "2025-05-01", "end_date": "2025-05-01", "related_type": "Museums"},
    {"name": "Janai Purnima Festival", "start_date": "2025-08-19", "end_date": "2025-08-19", "related_type": "Hindu Temples"},
    {"name": "Independence Day", "start_date": "2025-07-04", "end_date": "2025-07-04", "related_type": "Historical Sites"},
    {"name": "Republic Day", "start_date": "2025-05-28", "end_date": "2025-05-28", "related_type": "Museums"},
    {"name": "Bikram Sambat New Year", "start_date": "2025-04-14", "end_date": "2025-04-14", "related_type": "Parks"},
    {"name": "Autumn Festival", "start_date": "2025-09-23", "end_date": "2025-09-30", "related_type": "Caves"}
]
