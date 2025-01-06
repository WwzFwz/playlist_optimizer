import unittest
from playlist_optimizer import Song, MusicGraphOptimizer
from visualizer import print_playlist_analysis, generate_mermaid_graph

def create_test_songs():
    """Create sample songs for testing"""
    return [
        Song("1", "Bohemian Rhapsody", "Queen", 72, 0.9, 0.7, 0, 1, 354000),
        Song("2", "Uptown Funk", "Mark Ronson", 115, 0.8, 0.9, 4, 1, 270000),
        Song("3", "Sweet Child O' Mine", "Guns N' Roses", 125, 0.7, 0.6, 7, 1, 356000),
        Song("4", "Billie Jean", "Michael Jackson", 117, 0.8, 0.9, 2, 1, 294000)
    ]

def create_test_weights():
    """Create sample weights for parameters"""
    return {
        'tempo': 0.3,
        'energy': 0.25,
        'danceability': 0.2,
        'key': 0.15,
        'mode': 0.1
    }

class TestMusicPlaylistOptimizer(unittest.TestCase):
    def setUp(self):
        self.songs = create_test_songs()
        self.weights = create_test_weights()
        self.optimizer = MusicGraphOptimizer(self.songs, self.weights)

    def test_transition_cost(self):
        """Test transition cost calculation"""
        song1 = self.songs[0]
        song2 = self.songs[1]
        cost = self.optimizer.calculate_transition_cost(song1, song2)
        self.assertGreater(cost, 0)
        self.assertLess(cost, 1)

    def test_optimization(self):
        """Test playlist optimization"""
        optimized = self.optimizer.optimize_playlist(self.songs[0])
        self.assertEqual(len(optimized), len(self.songs))
        self.assertEqual(set(optimized), set(self.songs))
        self.assertEqual(optimized[0], self.songs[0])

    def test_total_cost(self):
        """Test total transition cost calculation"""
        playlist = self.songs
        total_cost = self.optimizer.calculate_total_transition_cost(playlist)
        manual_cost = sum(self.optimizer.calculate_transition_cost(playlist[i], playlist[i+1]) 
                         for i in range(len(playlist)-1))
        self.assertEqual(total_cost, manual_cost)

def main():
    """Run example optimization with visualization"""
    print("\nMENJALANKAN OPTIMASI PLAYLIST...")
    
    # Create test data
    songs = create_test_songs()
    weights = create_test_weights()
    optimizer = MusicGraphOptimizer(songs, weights)
    
    # Generate and print graph visualization
    print("\nVISUALISASI GRAF MUSIK:")
    print(generate_mermaid_graph(songs, optimizer))
    
    # Optimize playlist
    print("\nMEMULAI OPTIMASI...")
    optimized_playlist = optimizer.optimize_playlist(songs[0])
    
    # Print detailed analysis
    print_playlist_analysis(optimized_playlist, optimizer)

if __name__ == "__main__":
    # Run tests first
    print("MENJALANKAN UNIT TESTS...")
    unittest.main(argv=[''], exit=False)
    
    # Run example
    main()