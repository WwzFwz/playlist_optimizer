from song import Song
from playlist_optimizer import MusicGraphOptimizer
from visualizer import visualize_graph_matplotlib, print_playlist_analysis

def main():
    # Create sample songs
    songs = [
        Song("1", "Bohemian Rhapsody", "Queen", 72, 0.9, 0.7, 0, 1, 354000),
        Song("2", "Uptown Funk", "Mark Ronson", 115, 0.8, 0.9, 4, 1, 270000),
        Song("3", "Sweet Child O' Mine", "Guns N' Roses", 125, 0.7, 0.6, 7, 1, 356000),
        Song("4", "Billie Jean", "Michael Jackson", 117, 0.8, 0.9, 2, 1, 294000)
    ]
    
    # Create optimizer
    optimizer = MusicGraphOptimizer(songs)
    
    # Optimize playlist
    print("Optimizing playlist...")
    optimized_playlist = optimizer.optimize_playlist(songs[0])
    
    # Print analysis
    print_playlist_analysis(optimized_playlist, optimizer)
    
    # Create and show visualization
    plt = visualize_graph_matplotlib(optimized_playlist, optimizer)
    plt.show()

if __name__ == "__main__":
    main()