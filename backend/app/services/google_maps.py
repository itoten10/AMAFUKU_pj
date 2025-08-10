import googlemaps
import polyline as polyline_lib
from typing import List, Dict, Any, Optional
from app.core.config import settings
import random

class GoogleMapsService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    async def search_route(self, origin: str, destination: str) -> Dict[str, Any]:
        try:
            # Geocoding for origin and destination
            origin_geocode = self.client.geocode(origin, language='ja')
            dest_geocode = self.client.geocode(destination, language='ja')
            
            if not origin_geocode or not dest_geocode:
                return None
            
            origin_coords = {
                'lat': origin_geocode[0]['geometry']['location']['lat'],
                'lng': origin_geocode[0]['geometry']['location']['lng']
            }
            dest_coords = {
                'lat': dest_geocode[0]['geometry']['location']['lat'],
                'lng': dest_geocode[0]['geometry']['location']['lng']
            }
            
            # Get directions
            directions = self.client.directions(
                origin,
                destination,
                mode="driving",
                language="ja"
            )
            
            if not directions:
                return None
            
            route = directions[0]
            
            return {
                'origin': origin,
                'destination': destination,
                'origin_coords': origin_coords,
                'dest_coords': dest_coords,
                'distance': route['legs'][0]['distance']['text'],
                'duration': route['legs'][0]['duration']['text'],
                'polyline': route['overview_polyline']['points'],
                'steps': route['legs'][0]['steps']
            }
        except Exception as e:
            print(f"Error in search_route: {e}")
            return None
    
    async def get_historical_spots_along_route(
        self, 
        polyline: str, 
        num_points: int = 5
    ) -> List[Dict[str, Any]]:
        try:
            # Decode polyline to get route coordinates
            route_coords = polyline_lib.decode(polyline)
            
            # Sample points along the route
            sample_interval = max(1, len(route_coords) // (num_points + 1))
            sample_points = route_coords[::sample_interval][:num_points]
            
            historical_spots = []
            spot_ids = set()
            
            search_keywords = [
                "神社", "寺", "城", "史跡", "博物館", 
                "神社仏閣", "歴史的建造物", "文化財"
            ]
            
            for point in sample_points:
                keyword = random.choice(search_keywords)
                
                # Search for places near each point
                places_result = self.client.places_nearby(
                    location=(point[0], point[1]),
                    radius=5000,  # 5km radius
                    keyword=keyword,
                    language='ja'
                )
                
                for place in places_result.get('results', [])[:2]:  # Get up to 2 places per point
                    place_id = place.get('place_id')
                    if place_id and place_id not in spot_ids:
                        spot_ids.add(place_id)
                        
                        # Get detailed information
                        place_details = self.client.place(
                            place_id=place_id,
                            language='ja',
                            fields=['name', 'formatted_address', 'geometry', 'types']
                        )
                        
                        if place_details.get('result'):
                            details = place_details['result']
                            historical_spots.append({
                                'place_id': place_id,
                                'name': details.get('name', '不明な場所'),
                                'address': details.get('formatted_address', ''),
                                'lat': details['geometry']['location']['lat'],
                                'lng': details['geometry']['location']['lng'],
                                'types': details.get('types', []),
                                'description': self._generate_description(details.get('name', ''))
                            })
            
            return historical_spots
        except Exception as e:
            print(f"Error in get_historical_spots: {e}")
            # Return sample data if API fails
            return self._get_sample_historical_spots()
    
    def _generate_description(self, name: str) -> str:
        descriptions = {
            "神社": f"{name}は地域の守り神として古くから信仰されている神社です。",
            "寺": f"{name}は歴史ある寺院で、多くの参拝者が訪れます。",
            "城": f"{name}は戦国時代の歴史を今に伝える貴重な史跡です。",
            "博物館": f"{name}では地域の歴史や文化について学ぶことができます。",
        }
        
        for key, desc in descriptions.items():
            if key in name:
                return desc
        
        return f"{name}は歴史的に重要な場所として知られています。"
    
    def _get_sample_historical_spots(self) -> List[Dict[str, Any]]:
        return [
            {
                'place_id': 'sample_1',
                'name': '鎌倉大仏',
                'address': '神奈川県鎌倉市長谷',
                'lat': 35.3169,
                'lng': 139.5359,
                'types': ['tourist_attraction'],
                'description': '鎌倉大仏は13世紀に建立された国宝の仏像です。'
            },
            {
                'place_id': 'sample_2',
                'name': '鶴岡八幡宮',
                'address': '神奈川県鎌倉市雪ノ下',
                'lat': 35.3249,
                'lng': 139.5565,
                'types': ['shrine'],
                'description': '鶴岡八幡宮は鎌倉の守護神として古くから信仰されています。'
            }
        ]

google_maps_service = GoogleMapsService()