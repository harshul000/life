from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Destination data
DESTINATIONS = {
    "ladakh": {
        "id": "ladakh",
        "name": "Ladakh",
        "tagline": "Land of High Passes",
        "region": "Jammu & Kashmir",
        "coordinates": {"lat": 34.1526, "lng": 77.5771},
        "description": "Ladakh is a region in northern India known for its stunning landscapes, Buddhist monasteries, and adventure activities. The stark beauty of barren mountains, crystal-clear lakes, and ancient culture makes it a paradise for travelers.",
        "best_time": "May to September",
        "duration": "7-10 days",
        "highlights": [
            "Pangong Lake - Famous turquoise lake",
            "Nubra Valley - Sand dunes and double-humped camels",
            "Magnetic Hill - Gravity-defying phenomenon",
            "Thiksey Monastery - Beautiful Buddhist monastery",
            "Khardung La - One of the highest motorable passes"
        ],
        "activities": [
            "Trekking and hiking",
            "River rafting in Zanskar",
            "Motorcycle tours",
            "Monastery visits",
            "Stargazing",
            "Photography"
        ],
        "how_to_reach": "Fly to Leh (Kushok Bakula Rimpochee Airport) or take the scenic Manali-Leh highway",
        "tips": [
            "Acclimatize properly to avoid altitude sickness",
            "Carry warm clothing even in summer",
            "Book accommodations in advance during peak season",
            "Respect local culture and monasteries"
        ]
    },
    "spiti": {
        "id": "spiti",
        "name": "Spiti Valley",
        "tagline": "The Middle Land",
        "region": "Himachal Pradesh",
        "coordinates": {"lat": 32.2432, "lng": 78.0414},
        "description": "Spiti Valley is a cold desert mountain valley located high in the Himalayas. Known for its pristine beauty, ancient monasteries, and unique culture, Spiti offers an otherworldly experience.",
        "best_time": "May to October",
        "duration": "6-8 days",
        "highlights": [
            "Key Monastery - Largest monastery in Spiti",
            "Chandratal Lake - Moon Lake at 4,300m",
            "Kibber Village - One of the highest villages",
            "Pin Valley National Park - Snow leopard habitat",
            "Dhankar Monastery - Perched on a cliff"
        ],
        "activities": [
            "High-altitude trekking",
            "Monastery exploration",
            "Wildlife spotting",
            "Camping by Chandratal",
            "Village homestays",
            "Photography"
        ],
        "how_to_reach": "Drive from Manali via Rohtang Pass or from Shimla via Kinnaur",
        "tips": [
            "Roads are open only from May to October",
            "Carry sufficient cash as ATMs are scarce",
            "Respect local Buddhist culture",
            "Be prepared for basic facilities"
        ]
    },
    "munnar": {
        "id": "munnar",
        "name": "Munnar",
        "tagline": "Kashmir of South India",
        "region": "Kerala",
        "coordinates": {"lat": 10.0889, "lng": 77.0595},
        "description": "Munnar is a hill station in Kerala's Western Ghats, famous for its sprawling tea plantations, misty mountains, and pleasant climate. It's a perfect retreat for nature lovers.",
        "best_time": "September to May",
        "duration": "3-4 days",
        "highlights": [
            "Tea Gardens - Endless green carpets",
            "Eravikulam National Park - Nilgiri Tahr habitat",
            "Mattupetty Dam - Scenic reservoir",
            "Echo Point - Natural echo phenomenon",
            "Top Station - Panoramic views"
        ],
        "activities": [
            "Tea plantation tours",
            "Trekking",
            "Boating at Mattupetty",
            "Wildlife watching",
            "Photography",
            "Spice garden visits"
        ],
        "how_to_reach": "Nearest airport is Cochin (110 km). Drive through scenic mountain roads",
        "tips": [
            "Book tea plantation tours in advance",
            "Carry light woolens",
            "Try local Kerala cuisine",
            "Visit tea museums"
        ]
    },
    "ooty": {
        "id": "ooty",
        "name": "Ooty",
        "tagline": "Queen of Hill Stations",
        "region": "Tamil Nadu",
        "coordinates": {"lat": 11.4102, "lng": 76.6950},
        "description": "Ooty, officially Udhagamandalam, is a charming hill station in the Nilgiri Hills. Known for its colonial architecture, botanical gardens, and toy train, it's a classic hill station experience.",
        "best_time": "October to June",
        "duration": "2-3 days",
        "highlights": [
            "Nilgiri Mountain Railway - UNESCO Heritage toy train",
            "Botanical Gardens - 55 acres of flora",
            "Ooty Lake - Boating and picnics",
            "Doddabetta Peak - Highest point in Nilgiris",
            "Rose Garden - Thousands of rose varieties"
        ],
        "activities": [
            "Toy train ride",
            "Boating",
            "Garden visits",
            "Trekking",
            "Shopping for homemade chocolates",
            "Tea tasting"
        ],
        "how_to_reach": "Nearest airport is Coimbatore (88 km). Famous toy train from Mettupalayam",
        "tips": [
            "Book toy train tickets well in advance",
            "Try homemade chocolates",
            "Visit during flower show season",
            "Carry warm clothing"
        ]
    },
    "gokarna": {
        "id": "gokarna",
        "name": "Gokarna",
        "tagline": "Peaceful Beach Paradise",
        "region": "Karnataka",
        "coordinates": {"lat": 14.5479, "lng": 74.3188},
        "description": "Gokarna is a small temple town on Karnataka's coast, known for its pristine beaches and laid-back vibe. It's a perfect alternative to crowded Goa, offering peace and natural beauty.",
        "best_time": "October to March",
        "duration": "3-4 days",
        "highlights": [
            "Om Beach - Beach shaped like Om symbol",
            "Kudle Beach - Popular beach for relaxation",
            "Half Moon Beach - Secluded crescent beach",
            "Paradise Beach - Accessible only by boat/trek",
            "Mahabaleshwar Temple - Ancient Shiva temple"
        ],
        "activities": [
            "Beach hopping",
            "Swimming and surfing",
            "Beach camping",
            "Cliff jumping",
            "Yoga and meditation",
            "Temple visits"
        ],
        "how_to_reach": "Nearest airport is Goa (140 km) or train to Gokarna Road station",
        "tips": [
            "Respect local temple town culture",
            "Try beach shacks for fresh seafood",
            "Carry cash as ATMs are limited",
            "Trek between beaches for adventure"
        ]
    },
    "goa": {
        "id": "goa",
        "name": "Goa",
        "tagline": "India's Beach Capital",
        "region": "Goa",
        "coordinates": {"lat": 15.2993, "lng": 74.1240},
        "description": "Goa is India's smallest state, famous for its beautiful beaches, Portuguese heritage, vibrant nightlife, and water sports. It offers a perfect blend of relaxation and adventure.",
        "best_time": "November to February",
        "duration": "4-5 days",
        "highlights": [
            "Baga & Calangute Beach - Popular beaches",
            "Fort Aguada - 17th-century Portuguese fort",
            "Old Goa Churches - UNESCO World Heritage sites",
            "Dudhsagar Falls - Majestic waterfall",
            "Anjuna Flea Market - Shopping paradise"
        ],
        "activities": [
            "Water sports (parasailing, jet skiing)",
            "Beach parties and nightlife",
            "Portuguese heritage tours",
            "Spice plantation visits",
            "Dolphin watching",
            "Casino cruises"
        ],
        "how_to_reach": "Dabolim Airport or train to Madgaon/Thivim stations",
        "tips": [
            "Rent a scooter to explore freely",
            "Try Goan cuisine and seafood",
            "Book beach shacks in advance",
            "Explore both North and South Goa"
        ]
    },
    "alleppey": {
        "id": "alleppey",
        "name": "Alleppey (Alappuzha)",
        "tagline": "Venice of the East",
        "region": "Kerala",
        "coordinates": {"lat": 9.4981, "lng": 76.3388},
        "description": "Alleppey is famous for its backwaters, houseboat cruises, and serene canals. The network of lagoons, lakes, and canals offers a unique and tranquil experience.",
        "best_time": "November to February",
        "duration": "2-3 days",
        "highlights": [
            "Backwater Houseboat Cruise - Iconic experience",
            "Vembanad Lake - Largest lake in Kerala",
            "Alleppey Beach - Lighthouse and pier",
            "Kumarakom Bird Sanctuary - Bird watching",
            "Village backwater tours - Local life experience"
        ],
        "activities": [
            "Houseboat stays",
            "Canoe rides through villages",
            "Ayurvedic spa treatments",
            "Bird watching",
            "Village tours",
            "Kerala cuisine tasting"
        ],
        "how_to_reach": "Nearest airport is Cochin (53 km). Well connected by train and road",
        "tips": [
            "Book houseboats in advance",
            "Choose overnight houseboat for full experience",
            "Try traditional Kerala meals on houseboat",
            "Visit during Nehru Trophy Boat Race (August)"
        ]
    },
    "hampi": {
        "id": "hampi",
        "name": "Hampi",
        "tagline": "City of Ruins",
        "region": "Karnataka",
        "coordinates": {"lat": 15.3350, "lng": 76.4600},
        "description": "Hampi is a UNESCO World Heritage Site with magnificent ruins of the Vijayanagara Empire. The surreal landscape of giant boulders and ancient temples creates a magical atmosphere.",
        "best_time": "October to February",
        "duration": "2-3 days",
        "highlights": [
            "Virupaksha Temple - Active ancient temple",
            "Vittala Temple - Famous stone chariot",
            "Matanga Hill - Sunrise/sunset viewpoint",
            "Hampi Bazaar - Ancient marketplace",
            "Lotus Mahal - Indo-Islamic architecture"
        ],
        "activities": [
            "Temple exploration",
            "Boulder climbing",
            "Cycling through ruins",
            "Coracle rides on Tungabhadra",
            "Photography",
            "Sunset at Hemakuta Hill"
        ],
        "how_to_reach": "Nearest airport is Hubli (144 km). Train to Hospet (13 km from Hampi)",
        "tips": [
            "Rent a bicycle or scooter to explore",
            "Start early to avoid heat",
            "Hire a guide for historical context",
            "Stay in Hampi for authentic experience"
        ]
    },
    "manali": {
        "id": "manali",
        "name": "Manali",
        "tagline": "Valley of the Gods",
        "region": "Himachal Pradesh",
        "coordinates": {"lat": 32.2396, "lng": 77.1887},
        "description": "Manali is a high-altitude Himalayan resort town famous for its cool climate, snow-capped mountains, and adventure activities. It's a perfect destination for both adventure seekers and peace lovers.",
        "best_time": "October to June",
        "duration": "4-5 days",
        "highlights": [
            "Rohtang Pass - Snow-covered mountain pass",
            "Solang Valley - Adventure sports hub",
            "Hadimba Temple - Ancient wooden temple",
            "Old Manali - Hippie village vibe",
            "Beas River - Scenic riverside"
        ],
        "activities": [
            "Skiing and snowboarding",
            "Paragliding",
            "River rafting",
            "Trekking",
            "Mountain biking",
            "Cafe hopping in Old Manali"
        ],
        "how_to_reach": "Nearest airport is Bhuntar (50 km). Scenic drive from Delhi or Chandigarh",
        "tips": [
            "Book Rohtang Pass permits online in advance",
            "Visit Solang Valley for adventure sports",
            "Explore Old Manali for cafes and shopping",
            "Carry warm clothing year-round"
        ]
    },
    "shimla": {
        "id": "shimla",
        "name": "Shimla",
        "tagline": "Queen of Hills",
        "region": "Himachal Pradesh",
        "coordinates": {"lat": 31.1048, "lng": 77.1734},
        "description": "Shimla, the capital of Himachal Pradesh, is a classic colonial hill station with Victorian architecture, pleasant weather, and panoramic mountain views. It's perfect for a relaxed getaway.",
        "best_time": "March to June, December to February",
        "duration": "2-3 days",
        "highlights": [
            "The Mall Road - Colonial shopping street",
            "The Ridge - Open space with mountain views",
            "Jakhu Temple - Hanuman temple with views",
            "Kalka-Shimla Toy Train - UNESCO Heritage",
            "Christ Church - Neo-Gothic architecture"
        ],
        "activities": [
            "Toy train ride",
            "Mall Road shopping",
            "Heritage walks",
            "Trekking",
            "Ice skating (winter)",
            "Photography"
        ],
        "how_to_reach": "Nearest airport is Chandigarh (113 km). Famous toy train from Kalka",
        "tips": [
            "Book toy train tickets in advance",
            "Walk on Mall Road in evening",
            "Try local Himachali cuisine",
            "Visit nearby Kufri for snow activities"
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/destination/<destination_id>')
def destination(destination_id):
    if destination_id in DESTINATIONS:
        return render_template('destination.html', destination=DESTINATIONS[destination_id])
    return "Destination not found", 404

@app.route('/api/destinations')
def api_destinations():
    return jsonify(list(DESTINATIONS.values()))

@app.route('/api/destination/<destination_id>')
def api_destination(destination_id):
    if destination_id in DESTINATIONS:
        return jsonify(DESTINATIONS[destination_id])
    return jsonify({"error": "Destination not found"}), 404

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    for dest in DESTINATIONS.values():
        if (query in dest['name'].lower() or 
            query in dest['region'].lower() or 
            query in dest['description'].lower()):
            results.append(dest)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
