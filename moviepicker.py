# moviepicker.py
# A simple movie picker that randomly selects a film from user-chosen famous movie lists.

import random  # Import the random module to enable random movie selection

# ----------------------
# Define Movie Lists
# ----------------------

letterboxd_top_250 = [
    "Harakiri", "12 Angry Men", "Come and See", "Seven Samurai",
    "The Human Condition Part III", "High and Low",
    "The Godfather", "The Shawshank Redemption", "Parasite", "City of God"
]

imdb_top_250 = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight",
    "Schindler's List", "12 Angry Men",
    "The Lord of the Rings: The Return of the King",
    "Pulp Fiction", "The Lord of the Rings: The Fellowship of the Ring",
    "Inception"
]

afi_top_100 = [
    "Citizen Kane", "The Godfather", "Casablanca", "Raging Bull",
    "Singin' in the Rain", "Gone with the Wind",
    "Lawrence of Arabia", "Schindler's List", "Vertigo", "The Wizard of Oz"
]

# Store lists in a dictionary
lists = {
    "Letterboxd Top 250": letterboxd_top_250,
    "IMDB Top 250": imdb_top_250,
    "AFI Top 100": afi_top_100
}

# ----------------------
# Define Functions
# ----------------------

def show_available_lists():
    """Display available movie lists to the user."""
    print("Available Lists:\n")
    for i, list_name in enumerate(lists.keys(), start=1):
        print(f"{i}. {list_name}")

def get_user_choice():
    """Ask the user to select a list and return the selected list name."""
    choice = input("\nPlease select a list: ")
    try:
        choice_index = int(choice) - 1
        if choice_index < 0 or choice_index >= len(lists):
            raise ValueError("Invalid choice.")
        selected_list_name = list(lists.keys())[choice_index]
        return selected_list_name
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid number between 1 and {len(lists)}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Please try again.")
        return None

def pick_random_movie(movie_list):
    """Select and return a random movie from the given list."""
    return random.choice(movie_list)

def main():
    """Main program loop."""
    print("Welcome to the Movie Picker!\n")
    show_available_lists()
    
    selected_list_name = get_user_choice()
    if selected_list_name:
        selected_list = lists[selected_list_name]
        random_movie = pick_random_movie(selected_list)
        print(f"\nYou should watch: {random_movie} from {selected_list_name}!\n")

# ----------------------
# Run the Program
# ----------------------
if __name__ == "__main__":
    main()
