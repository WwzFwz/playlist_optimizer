class Song:
    def __init__(self, id: str, title: str, artist: str, 
                 tempo: float, energy: float, danceability: float, 
                 key: int, mode: int, duration_ms: int):
        self.id = id
        self.title = title
        self.artist = artist
        self.tempo = tempo      # BPM
        self.energy = energy    # 0.0 to 1.0
        self.danceability = danceability
        self.key = key         # 0-11 (C=0, C#=1, etc.)
        self.mode = mode       # Major (1) or minor (0)
        self.duration_ms = duration_ms
        
    def __str__(self):
        return f"{self.title} - {self.artist}"
        
    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        return self.id == other.id
        
    def __hash__(self):
        return hash(self.id)