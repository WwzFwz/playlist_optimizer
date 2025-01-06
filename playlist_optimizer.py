# import numpy as np
# from typing import List, Dict, Set, Tuple
# import heapq

# class Song:
#     def __init__(self, id: str, title: str, artist: str, 
#                  tempo: float, energy: float, danceability: float, 
#                  key: int, mode: int, duration_ms: int):
#         self.id = id
#         self.title = title
#         self.artist = artist
#         self.tempo = tempo  # BPM
#         self.energy = energy  # 0.0 to 1.0
#         self.danceability = danceability  # 0.0 to 1.0
#         self.key = key  # 0-11 (C=0, C#=1, etc.)
#         self.mode = mode  # Major (1) or minor (0)
#         self.duration_ms = duration_ms
        
#     def __str__(self):
#         return f"{self.title} - {self.artist}"

# class PlaylistNode:
#     def __init__(self, songs: List[Song], current_song: Song):
#         self.songs = songs  # List of songs in current path
#         self.current_song = current_song
        
#     def __lt__(self, other):
#         return len(self.songs) < len(other.songs)

# class MusicGraphOptimizer:
#     def __init__(self, songs: List[Song], weights: Dict[str, float]):
#         self.songs = songs
#         self.weights = weights
        
#     def calculate_transition_cost(self, song1: Song, song2: Song) -> float:
#         """Calculate the weighted transition cost between two songs."""
#         costs = {
#             'tempo': abs(song1.tempo - song2.tempo) / 200.0,
#             'energy': abs(song1.energy - song2.energy),
#             'danceability': abs(song1.danceability - song2.danceability),
#             'key': min((song1.key - song2.key) % 12, (song2.key - song1.key) % 12) / 12.0,
#             'mode': abs(song1.mode - song2.mode)
#         }
#         return sum(self.weights[param] * cost for param, cost in costs.items())

#     def heuristic(self, current: Song, remaining: Set[Song]) -> float:
#         """Estimate remaining cost using admissible heuristic."""
#         if not remaining:
#             return 0
#         min_cost = float('inf')
#         for song in remaining:
#             cost = self.calculate_transition_cost(current, song)
#             min_cost = min(min_cost, cost)
#         return min_cost * len(remaining)

#     def optimize_playlist(self, start_song: Song) -> List[Song]:
#         """Use A* to find optimal playlist ordering."""
#         open_set = []
#         closed_set = set()
        
#         start_node = PlaylistNode([start_song], start_song)
#         remaining_songs = set(self.songs) - {start_song}
        
#         heapq.heappush(open_set, (self.heuristic(start_song, remaining_songs), start_node))
        
#         while open_set:
#             current_f, current_node = heapq.heappop(open_set)
            
#             if len(current_node.songs) == len(self.songs):
#                 return current_node.songs
                
#             node_key = (current_node.current_song.id, 
#                        tuple(song.id for song in current_node.songs))
            
#             if node_key in closed_set:
#                 continue
                
#             closed_set.add(node_key)
            
#             remaining = set(self.songs) - set(current_node.songs)
#             for next_song in remaining:
#                 g_score = current_f - self.heuristic(current_node.current_song, remaining)
#                 g_score += self.calculate_transition_cost(current_node.current_song, next_song)
                
#                 new_songs = current_node.songs + [next_song]
#                 new_node = PlaylistNode(new_songs, next_song)
                
#                 f_score = g_score + self.heuristic(next_song, remaining - {next_song})
#                 heapq.heappush(open_set, (f_score, new_node))
        
#         return []

#     def calculate_total_transition_cost(self, playlist: List[Song]) -> float:
#         """Calculate total transition cost for a playlist."""
#         return sum(self.calculate_transition_cost(playlist[i], playlist[i+1]) 
#                   for i in range(len(playlist)-1))


import heapq
from typing import List, Set, Dict, Tuple
from song import Song

class PlaylistNode:
    def __init__(self, songs: List[Song], current_song: Song):
        self.songs = songs  # List of songs in current path
        self.current_song = current_song
        
    def __lt__(self, other):
        return len(self.songs) < len(other.songs)

class MusicGraphOptimizer:
    def __init__(self, songs: List[Song], weights: Dict[str, float] = None):
        self.songs = songs
        self.weights = weights or {
            'tempo': 0.3,
            'energy': 0.25,
            'danceability': 0.2,
            'key': 0.15,
            'mode': 0.1
        }
        
    def calculate_transition_cost(self, song1: Song, song2: Song) -> float:
        """Calculate the weighted transition cost between two songs."""
        costs = {
            'tempo': abs(song1.tempo - song2.tempo) / 200.0,
            'energy': abs(song1.energy - song2.energy),
            'danceability': abs(song1.danceability - song2.danceability),
            'key': min((song1.key - song2.key) % 12, (song2.key - song1.key) % 12) / 12.0,
            'mode': abs(song1.mode - song2.mode)
        }
        return sum(self.weights[param] * cost for param, cost in costs.items())

    def heuristic(self, current: Song, remaining: Set[Song]) -> float:
        """Estimate remaining cost using admissible heuristic."""
        if not remaining:
            return 0
        min_cost = float('inf')
        for song in remaining:
            cost = self.calculate_transition_cost(current, song)
            min_cost = min(min_cost, cost)
        return min_cost * len(remaining)

    def optimize_playlist(self, start_song: Song) -> List[Song]:
        """Use A* to find optimal playlist ordering."""
        open_set = []
        closed_set = set()
        
        start_node = PlaylistNode([start_song], start_song)
        remaining_songs = set(self.songs) - {start_song}
        
        heapq.heappush(open_set, (self.heuristic(start_song, remaining_songs), start_node))
        
        while open_set:
            current_f, current_node = heapq.heappop(open_set)
            
            if len(current_node.songs) == len(self.songs):
                return current_node.songs
                
            node_key = (current_node.current_song.id, 
                       tuple(song.id for song in current_node.songs))
            
            if node_key in closed_set:
                continue
                
            closed_set.add(node_key)
            
            remaining = set(self.songs) - set(current_node.songs)
            for next_song in remaining:
                g_score = current_f - self.heuristic(current_node.current_song, remaining)
                g_score += self.calculate_transition_cost(current_node.current_song, next_song)
                
                new_songs = current_node.songs + [next_song]
                new_node = PlaylistNode(new_songs, next_song)
                
                f_score = g_score + self.heuristic(next_song, remaining - {next_song})
                heapq.heappush(open_set, (f_score, new_node))
        
        return []  # No solution found

    def calculate_total_cost(self, playlist: List[Song]) -> float:
        """Calculate total transition cost for a playlist."""
        return sum(self.calculate_transition_cost(playlist[i], playlist[i+1]) 
                  for i in range(len(playlist)-1))