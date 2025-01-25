import matplotlib.pyplot as plt
import matplotlib.animation as animation
import algo
import numpy as np


def get_integer_input(prompt, default=None, min_value=None, max_value=None):
    """
    Prompts the user for an integer input with validation and default handling.
    """
    while True:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        if not user_input and default is not None:
            return default
        try:
            value = int(user_input)
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Please enter a value between {min_value} and {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_sorting_method():
    """
    Prompts the user to select a sorting method with validation.
    """
    methods = {
        "b": "Bubble sort",
        "i": "Insertion sort",
        "m": "Merge sort",
        "q": "Quicksort",
        "s": "Selection sort"
    }
    print("Choose a sorting method:")
    for key, name in methods.items():
        print(f"  ({key}) {name}")
    
    while True:
        method = input("Enter your choice: ").strip().lower()
        if method in methods:
            return method, methods[method]
        print("Invalid choice. Please choose a valid sorting method.")


if __name__ == "__main__":
    # Get user input to determine range of integers (1 to N) and desired
    # Get user inputs with validation
    N = get_integer_input("Enter the number of integers to sort", default=50, min_value=2, max_value=500)
    method, title = get_sorting_method()

    # Build and shuffle the list of integers
    A = np.random.randint(1, 2 * N, N)

    # Get the appropriate generator
    if method == "b":
        generator = algo.bubblesort(A)
    elif method == "i":
        generator = algo.insertionsort(A)
    elif method == "m":
        generator = algo.mergesort(A, 0, N - 1)
    elif method == "q":
        generator = algo.quicksort(A, 0, N - 1)
    else:
        generator = algo.selectionsort(A)


    # Initialize figure and axis.
    fig, ax = plt.subplots()
    ax.set_title(title)

    # Initialize a bar plot. Note that matplotlib.pyplot.bar() returns a
    # list of rectangles (with each bar in the bar plot corresponding
    # to one rectangle), which we store in bar_rects.
    bar_rects = ax.bar(range(len(A)), A, align="edge")

    # Set axis limits. Set y axis upper limit high enough that the tops of
    # the bars won't overlap with the text label.
    ax.set_xlim(0, N)
    ax.set_ylim(0, int(2.07 * N))

    # Place a text label in the upper-left corner of the plot to display
    # number of operations performed by the sorting algorithm (each "yield"
    # is treated as 1 operation).
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    # Define function update_fig() for use with matplotlib.pyplot.FuncAnimation().
    # To track the number of operations, i.e., iterations through which the
    # animation has gone, define a variable "iteration". This variable will
    # be passed to update_fig() to update the text label, and will also be
    # incremented in update_fig(). For this increment to be reflected outside
    # the function, we make "iteration" a list of 1 element, since lists (and
    # other mutable objects) are passed by reference (but an integer would be
    # passed by value).
    # NOTE: Alternatively, iteration could be re-declared within update_fig()
    # with the "global" keyword (or "nonlocal" keyword).
    iteration = [0]
    def update_fig(A, rects, iteration):
        for rect, val in zip(rects, A):
            rect.set_height(val)
            rect.set_color(plt.cm.viridis(val / max(A)))  # Update bar color dynamically
        iteration[0] += 1
        text.set_text(f"# of operations: {iteration[0]}")

    # Animation
    anim = animation.FuncAnimation(
        fig, func=update_fig, fargs=(bar_rects, iteration),
        frames=generator, interval=200, repeat=False, cache_frame_data=False
    )
    plt.show()