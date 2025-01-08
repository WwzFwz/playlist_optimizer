from typing import List
import matplotlib.pyplot as plt
import networkx as nx
from song import Song
from playlist_optimizer import MusicGraphOptimizer

def get_key_name(key: int) -> str:
    """Convert numeric key to name"""
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return keys[key]

def visualize_graph_matplotlib(playlist: List[Song], optimizer: MusicGraphOptimizer):
    """Create graph visualization using matplotlib with clear path indication"""
    # Buat graph
    G = nx.DiGraph()
    
    # Tambahkan nodes (lagu-lagu)
    for i, song in enumerate(playlist):
        G.add_node(song.title, 
                  tempo=song.tempo,
                  key=get_key_name(song.key),
                  position=i)
    
    # Tambahkan edges (transisi antar lagu)
    for song1 in playlist:
        for song2 in playlist:
            if song1 != song2:
                cost = optimizer.calculate_transition_cost(song1, song2)
                G.add_edge(song1.title, song2.title, weight=cost)
    
    # Setup plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Gambar semua edges dengan warna abu-abu
    nx.draw_networkx_edges(G, pos,
                          edge_color='lightgray',
                          width=1,
                          alpha=0.3)
    
    # Gambar jalur optimal dengan warna merah
    optimal_edges = [(playlist[i].title, playlist[i+1].title) 
                    for i in range(len(playlist)-1)]
    
    nx.draw_networkx_edges(G, pos,
                          edgelist=optimal_edges,
                          edge_color='red',
                          width=2)
    
    # Gambar nodes dengan warna berbeda untuk start dan end
    node_colors = []
    for node in G.nodes():
        if node == playlist[0].title:  # Start node (hijau)
            node_colors.append('lightgreen')
        elif node == playlist[-1].title:  # End node (pink)
            node_colors.append('lightpink')
        else:  # Node tengah (biru)
            node_colors.append('lightblue')
    
    # Gambar nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=2000,
                          alpha=0.7)
    
    # Tambahkan label untuk nodes
    labels = {node: f"{node}\nBPM: {G.nodes[node]['tempo']}\nKey: {G.nodes[node]['key']}"
             for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Tambahkan label untuk edges (cost transisi)
    edge_labels = {(u,v): f"{G[u][v]['weight']:.3f}"
                  for u,v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)
    
    # Tambahkan legenda
    plt.plot([], [], color='lightgreen', marker='o', markersize=15, 
            label='Start: ' + playlist[0].title, linestyle='None')
    plt.plot([], [], color='lightpink', marker='o', markersize=15, 
            label='End: ' + playlist[-1].title, linestyle='None')
    plt.plot([], [], color='red', linewidth=2, 
            label='Optimal Path')
    
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.title("Playlist Transition Graph\nPanah merah menunjukkan urutan optimal")
    plt.axis('off')
    plt.tight_layout()
    
    return plt

def print_playlist_analysis(playlist: List[Song], optimizer: MusicGraphOptimizer):
    """Print detailed analysis of playlist transitions"""
    print("\nANALISIS PLAYLIST")
    print("=" * 50)
    
    total_cost = 0
    for i, song in enumerate(playlist, 1):
        print(f"\n{i}. {song.title} - {song.artist}")
        print(f"   ├─ Tempo: {song.tempo} BPM")
        print(f"   ├─ Key: {get_key_name(song.key)} {'Major' if song.mode == 1 else 'Minor'}")
        print(f"   ├─ Energy: {song.energy:.2f}")
        print(f"   └─ Danceability: {song.danceability:.2f}")
        
        if i < len(playlist):
            cost = optimizer.calculate_transition_cost(song, playlist[i])
            total_cost += cost
            print(f"\n   Transisi ke {playlist[i].title}:")
            print(f"   └─ Cost: {cost:.3f}")
    
    print(f"\nTotal cost transisi: {total_cost:.3f}")
    print(f"Rata-rata cost transisi: {total_cost/(len(playlist)-1):.3f}")


def print_analysis(playlist: List[Song], optimizer: MusicGraphOptimizer):
    """Print complete analysis with all required tables"""
    
    # Table I: Detail Path Optimal dan Transisi
    print("\nTABEL I: DETAIL PATH OPTIMAL DAN TRANSISI")
    print("="*80)
    print(f"{'Urutan':<8} | {'Lagu':<20} | {'Next':<20} | {'Cost':<8} | {'Detail Parameter':<20}")
    print("-"*80)
    
    for i in range(len(playlist)-1):
        song1 = playlist[i]
        song2 = playlist[i+1]
        cost = optimizer.calculate_transition_cost(song1, song2)
        tempo_diff = abs(song2.tempo - song1.tempo)
        key_diff = min((song2.key - song1.key) % 12, (song1.key - song2.key) % 12)
        
        print(f"{i+1:<8} | {song1.title:<20} | {song2.title:<20} | {cost:.3f} | Δ Tempo: {tempo_diff:+.0f} BPM, ΔKey: {key_diff:+d}")
    
    # Table II: Perbandingan Path
    print("\nTABEL II: PERBANDINGAN BERBAGAI PATH")
    print("="*80)
    print(f"{'Path':<30} | {'Total Cost':<10} | {'Avg Cost':<10} | {'Max Cost':<10} | {'Min Cost':<10}")
    print("-"*80)
    
    # Calculate costs for current path
    costs = [optimizer.calculate_transition_cost(playlist[i], playlist[i+1]) 
             for i in range(len(playlist)-1)]
    total_cost = sum(costs)
    avg_cost = total_cost / len(costs)
    max_cost = max(costs)
    min_cost = min(costs)
    
    print(f"{'Path A* (Optimal)':<30} | {total_cost:.3f} | {avg_cost:.3f} | {max_cost:.3f} | {min_cost:.3f}")
    
    # Table III: Analisis Parameter Musik
    print("\nTABEL III: ANALISIS PARAMETER MUSIK")
    print("="*80)
    print(f"{'Parameter':<12} | {'Bobot':<8} | {'Rata-rata':<10} | {'Std Dev':<8} | {'Impact':<8}")
    print("-"*80)
    
    parameters = {
        'Tempo': {'weight': 0.3, 'values': []},
        'Energy': {'weight': 0.25, 'values': []},
        'Dance': {'weight': 0.2, 'values': []},
        'Key': {'weight': 0.15, 'values': []},
        'Mode': {'weight': 0.1, 'values': []}
    }
    
    # Calculate parameter changes
    for i in range(len(playlist)-1):
        song1, song2 = playlist[i], playlist[i+1]
        parameters['Tempo']['values'].append(abs(song2.tempo - song1.tempo))
        parameters['Energy']['values'].append(abs(song2.energy - song1.energy))
        parameters['Dance']['values'].append(abs(song2.danceability - song1.danceability))
        parameters['Key']['values'].append(min((song2.key - song1.key) % 12, 
                                             (song1.key - song2.key) % 12))
        parameters['Mode']['values'].append(abs(song2.mode - song1.mode))
    
    for param, data in parameters.items():
        values = data['values']
        if values:
            mean = sum(values) / len(values)
            std_dev = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
            impact = data['weight'] * mean
            print(f"{param:<12} | {data['weight']:.2f} | {mean:>10.3f} | {std_dev:>8.3f} | {impact:>8.3f}")

    print("\nNote: Impact dihitung dari weight * rata-rata perubahan parameter")


def generate_alternative_paths(playlist: List[Song], optimizer: MusicGraphOptimizer):
    """Generate alternative paths for comparison"""
    # Alternative path 1: Start -> End -> Mid songs
    alt_path1 = [playlist[0], playlist[-1]] + playlist[1:-1]
    
    # Alternative path 2: Reverse order of optimal path
    alt_path2 = playlist[::-1]
    
    return [
        ("Path A* (Optimal)", playlist),
        ("Path Alternatif 1", alt_path1),
        ("Path Alternatif 2", alt_path2)
    ]

def print_path_comparison(paths, optimizer: MusicGraphOptimizer):
    """Print comparison table of different paths"""
    print("\nTABEL II: PERBANDINGAN BERBAGAI PATH")
    print("="*80)
    print(f"{'Path':<40} | {'Total Cost':<10} | {'Avg Cost':<10} | {'Max Cost':<10} | {'Min Cost':<10}")
    print("-"*80)
    
    for path_name, path in paths:
        # Calculate costs for path
        costs = [optimizer.calculate_transition_cost(path[i], path[i+1]) 
                for i in range(len(path)-1)]
        
        total_cost = sum(costs)
        avg_cost = total_cost / len(costs)
        max_cost = max(costs)
        min_cost = min(costs)
        
        # Print path details
        path_str = " → ".join([song.title[:10] for song in path])
        print(f"{path_str:<40} | {total_cost:.3f} | {avg_cost:.3f} | {max_cost:.3f} | {min_cost:.3f}")

    print("\nDetail urutan setiap path:")
    for path_name, path in paths:
        print(f"\n{path_name}:")
        for i, song in enumerate(path):
            print(f"{i+1}. {song.title}")