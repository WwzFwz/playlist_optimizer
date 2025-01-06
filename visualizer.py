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



