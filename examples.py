"""
Test and example usage of the Embeddings API

This script demonstrates how to use the API endpoints programmatically
without needing the server running (for testing purposes).
"""

from embeddings import create_embedding, get_embedding_dimension
from similarity import rank_events_by_similarity


def example_create_embeddings():
    """Example: Create embeddings for texts"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Creating Embeddings")
    print("="*60)
    
    texts = [
        "I love hiking and outdoor adventures",
        "I enjoy programming and coding",
        "I like cooking and trying new recipes"
    ]
    
    try:
        embedding_dim = get_embedding_dimension()
        print(f"\nEmbedding Dimension: {embedding_dim}\n")
        
        embeddings = {}
        for text in texts:
            embedding = create_embedding(text)
            embeddings[text] = embedding
            print(f"Text: {text}")
            print(f"Embedding (first 10 values): {embedding[:10]}")
            print(f"Embedding length: {len(embedding)}\n")
        
        return embeddings
    except Exception as e:
        print(f"Error: {e}")
        return {}


def example_compare_events(user_embedding):
    """Example: Compare user profile with events"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Comparing User Profile with Events")
    print("="*60)
    
    # Create event embeddings
    events_data = [
        ("event_1", "Hiking Trail Adventure", "Join us for hiking in the mountains"),
        ("event_2", "Cooking Workshop", "Learn to cook Italian cuisine"),
        ("event_3", "Programming Bootcamp", "Intensive 10-week coding program"),
        ("event_4", "Nature Walk", "Peaceful walk through forest trails"),
        ("event_5", "Web Development Course", "Learn HTML, CSS, and JavaScript"),
    ]
    
    try:
        print(f"\nUser Profile Embedding: {user_embedding[:10]}...")
        print(f"\nComparing user with {len(events_data)} events:\n")
        
        # Create embeddings for events
        event_embeddings = []
        for event_id, name, description in events_data:
            embedding = create_embedding(description)
            event_embeddings.append((event_id, name, description, embedding))
        
        # Rank events by similarity
        ranked = rank_events_by_similarity(user_embedding, event_embeddings)
        
        print("Results (sorted by similarity):\n")
        print(f"{'Rank':<6} {'Event ID':<10} {'Name':<25} {'Similarity':<12}")
        print("-" * 60)
        
        for rank, (event_id, name, description, similarity) in enumerate(ranked, 1):
            print(f"{rank:<6} {event_id:<10} {name:<25} {similarity:.4f}")
        
        print("\nDetailed Results:")
        for rank, (event_id, name, description, similarity) in enumerate(ranked, 1):
            print(f"\n{rank}. {name} (Score: {similarity:.4f})")
            print(f"   Event ID: {event_id}")
            print(f"   Description: {description}")
        
        return ranked
    except Exception as e:
        print(f"Error: {e}")
        return []


def example_similarity_interpretation():
    """Show example of similarity score interpretation"""
    print("\n" + "="*60)
    print("SIMILARITY SCORE INTERPRETATION")
    print("="*60)
    
    interpretations = [
        (0.90, "Very High", "Almost identical meaning"),
        (0.75, "High", "Very similar topics"),
        (0.50, "Medium", "Related but different aspects"),
        (0.25, "Low", "Loosely related"),
        (0.0, "Very Low", "No similarity or unrelated"),
    ]
    
    print(f"\n{'Score':<8} {'Level':<15} {'Interpretation':<35}")
    print("-" * 60)
    for score, level, interpretation in interpretations:
        print(f"{score:<8.2f} {level:<15} {interpretation:<35}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Embeddings API - Example Usage".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Example 1: Create embeddings
        embeddings = example_create_embeddings()
        
        if embeddings:
            # Use the first embedding as user profile
            user_embedding = list(embeddings.values())[0]
            
            # Example 2: Compare events
            example_compare_events(user_embedding)
        
        # Example 3: Interpretation guide
        example_similarity_interpretation()
        
        print("\n" + "="*60)
        print("Examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nError during examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
