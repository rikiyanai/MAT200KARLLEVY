import cmath
import itertools
import re
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.pyplot import scatter
from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib.widgets import Button
import numpy as np
import tkinter as tk
from tkinter import ttk
import os
import sys
import colorama
from colorama import Fore, Style
import random
import time
from matplotlib.animation import FuncAnimation, Animation



def get_unique_colors(n): #Input: n = Length of number of integers in the list of unique of coefficients
    colors = []
    for i in range(n):
        color = "#%06x" % random.randint(0, 0xFFFFFF)#generate random color in hex & assign variable color eg."#ffffff"
        colors.append(color)
    return colors #Output: List of unique colors for each integer in the list of unique coefficients
    
def quadratic_roots(a, b, c): #Input: a, b, c = Coefficients of the quadratic equation
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        root1 = (-b + np.sqrt(discriminant)) / (2*a)
        root2 = (-b - np.sqrt(discriminant)) / (2*a)
        return root1, root2    #Output: Real roots of the quadratic equation
    else:
        real_part = -b / (2*a)
        imag_part = np.sqrt(-discriminant) / (2*a)
        return complex(real_part, imag_part), complex(real_part, -imag_part) #Output: Complex roots of the quadratic equation


def plot_roots(permutations):
    # Create a figure with two subplots: one 3D plot and one 2D plot
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d', facecolor='grey')
    ax2 = fig.add_subplot(122, facecolor='black')

    # Initialize lists to store real and complex roots
    real_roots = []
    complex_roots = []

    # Iterate over each permutation of coefficients
    for i, (a, b, c) in enumerate(permutations):
        # Calculate the roots of the quadratic equation
        root1, root2 = quadratic_roots(a, b, c)
        
        # Check if the roots are real or complex
        if isinstance(root1, complex) or isinstance(root2, complex):
            # If complex, add both roots to the complex_roots list
            complex_roots.append((root1, i+1))
            complex_roots.append((root2, i+1))
        else:
            # If real, add both roots to the real_roots list
            real_roots.append((root1, i+1))
            real_roots.append((root2, i+1))

    # Convert the real_roots and complex_roots lists to numpy arrays
    real_roots = np.array(real_roots)
    complex_roots = np.array(complex_roots)

    # Plot the real roots in the 3D plot
    ax1.scatter(real_roots[:, 0], np.zeros_like(real_roots[:, 0]), 0, color='lime', label='Real Roots')
    
    # Plot the complex roots in the 3D plot
    ax1.scatter(complex_roots[:, 0].real, complex_roots[:, 0].imag, 0, color='orange', label='Complex Roots')
    
    # Set labels and colors for the 3D plot
    ax1.set_xlabel('Real x axis', color='white')
    ax1.set_zlabel('Real y axis', color='white')
    ax1.set_ylabel('Imaginary axis', color='white')
    ax1.legend(facecolor='Gray', edgecolor='white', labelcolor='white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.tick_params(axis='z', colors='white')
    ax1.xaxis.set_pane_color((0, 0, 0, 1.0))
    ax1.yaxis.set_pane_color((0, 0, 0, 1.0))
    ax1.zaxis.set_pane_color((0, 0, 0, 1.0))

    # Plot the real roots in the 2D plot
    ax2.scatter(real_roots[:, 0], np.zeros_like(real_roots[:, 0]), color='lime', label='Real Roots')
    
    # Plot the complex roots in the 2D plot
    ax2.scatter(complex_roots[:, 0].real, complex_roots[:, 0].imag, color='orange', label='Complex Roots')
    
    # Set labels and colors for the 2D plot
    ax2.set_xlabel('Real x axis', color='white')
    ax2.set_ylabel('Imaginary axis', color='white')
    ax2.legend(facecolor='black', edgecolor='white', labelcolor='white')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    # Create a dictionary to store equation labels
    equation_labels = {i+1: f'Eq#{i+1}' for i in range(len(permutations))}

    # Create a dictionary to store annotations
    annotations = {}

    # Function to handle hover events
    def on_hover(event):
        if event.inaxes == ax1 or event.inaxes == ax2:
            for root, eq_num in np.concatenate((real_roots, complex_roots)):
                if event.inaxes == ax1:
                    data_point_location = scatter.get_offsets()[['eq_num'][0]]
                    if np.abs(event.xdata - root.real) < 0.1 and np.abs(event.ydata - root.imag) < 0.1:
                        if eq_num not in annotations:
                            annotations[eq_num] = event.inaxes.annotate(
                                equation_labels[eq_num],
                                xy=(root.real, root.imag),
                                xytext=(10, 10),
                                textcoords=data_point_location,
                                color='white',
                                ha='left',
                                va='bottom',
                                bbox=dict(boxstyle='round,pad=0.5', fc='black', ec='white', alpha=0.7),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='white')
                            )
                        else:
                            annotations[eq_num].set_visible(True)
                    fig.canvas.draw_idle()
                    return
                elif event.inaxes == ax2:
                    if np.abs(event.xdata - root.real) < 0.1 and np.abs(event.ydata - root.imag) < 0.1:
                        if eq_num not in annotations:
                            annotations[eq_num] = event.inaxes.annotate(
                                equation_labels[eq_num],
                                xy=(root.real, root.imag),
                                xytext=(10, 10),
                                textcoords='offset points',
                                color='white',
                                ha='left',
                                va='bottom',
                                bbox=dict(boxstyle='round,pad=0.5', fc='black', ec='white', alpha=0.7),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='white')
                            )
                        else:
                            annotations[eq_num].set_visible(True)
                    fig.canvas.draw_idle()
                    return

        for eq_num in annotations:
            annotations[eq_num].set_visible(False)
        fig.canvas.draw_idle()

    # Connect the hover event to the figure canvas
    fig.canvas.mpl_connect('motion_notify_event', on_hover)

    # Variable to track the visibility of parabolas
    parabolas_visible = False

    # Function to toggle the visibility of parabolas
    def plot_parabolas(event):
        nonlocal parabolas_visible
        if not parabolas_visible:
            x = np.linspace(-10, 10, 100)
            for i, (a, b, c) in enumerate(permutations):
                y = a*x**2 + b*x + c
                color = 'lime' if i < len(real_roots) // 2 else 'orange'
                ax1.plot(x, np.zeros_like(x), y, color=color, alpha=0.5)
            parabolas_visible = True
        else:
            ax1.clear()
            ax1.scatter(real_roots[:, 0], np.zeros_like(real_roots[:, 0]), 0, color='lime', label='Real Roots')
            ax1.scatter(complex_roots[:, 0].real, complex_roots[:, 0].imag, 0, color='orange', label='Complex Roots')
            ax1.set_xlabel('Real x axis', color='white')
            ax1.set_zlabel('Real y axis', color='white')
            ax1.set_ylabel('Imaginary axis', color='white')
            ax1.legend(facecolor='black', edgecolor='white', labelcolor='white')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            ax1.tick_params(axis='z', colors='white')
            ax1.xaxis.set_pane_color((0, 0, 0, 1.0))
            ax1.yaxis.set_pane_color((0, 0, 0, 1.0))
            ax1.zaxis.set_pane_color((0, 0, 0, 1.0))
            parabolas_visible = False
        plt.draw()

    # Create a button to toggle the visibility of parabolas
    ax_button_parabola = plt.axes([0.7, 0.01, 0.2, 0.06], facecolor='black')
    button_parabola = Button(ax_button_parabola, 'Toggle Parabolas', color='white', hovercolor='gray')
    button_parabola.label.set_color('black')
    button_parabola.on_clicked(plot_parabolas)

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()  



# This function prompts the user to enter a range of integers and returns the list of integers in that range
def get_coefficients():
    while True:
        try:
            # Prompt the user to enter a range of integers in the format a,b
            input_str = input("\033[1;32m>> Enter a range of integers in the format a,b: \033[0m")
            # Split the input string by comma and convert the resulting substrings to integers
            a, b = map(int, input_str.split(','))
            break
        except ValueError:
            print("Invalid input. Please enter a valid range of integers.")

    # Create a list of integers from a to b (inclusive)
    intArray = list(range(a, b + 1))
    # Get a list of unique colors based on the length of intArray
    color_array = get_unique_colors(len(intArray))
    # Create a dictionary that maps each integer in intArray to a color from color_array
    color_of_coefficient = {i: color for i, color in zip(intArray, color_array)}

    return intArray, color_of_coefficient

def find_unique_3_tuples(intArray):
    unique_3_tuples = list(combinations(intArray, 3))
    return unique_3_tuples

def find_permutations(unique_3_tuples):

    permutations = []
    for tuple in unique_3_tuples:
        tuple_permutations = list(itertools.permutations(tuple))
        permutations.extend(tuple_permutations)
    return permutations

def menu_options():
    print(" ")
    print("\033[1;32m>> 1. re enter range of integers\033[0m")
    print("\033[1;32m>> 2. print all the equations & roots in the range\033[0m")
    print("\033[1;32m>> 3. visualize\033[0m")
    print("\033[1;32m>> 4. Quit\033[0m")
    choice = input(">> Enter choice: ")
    return choice

#UX functions
def format_quote(quote):
    # ANSI escape sequences for colors
    RESET = '\033[0m'  # Reset all text formatting
    DARK_ULTRAMARINE_BLUE_BG = '\033[48;5;0m'  # Set background color to dark ultramarine blue
    YELLOW = '\033[92m'  # Set text color to yellow

    formatted_quote = ''  # Initialize an empty string to store the formatted quote
    for char in quote:  # Iterate over each character in the input quote
        if char == '|':  # If the character is '|'
            # Generate a random color for the '|' character
            random_color = f'\033[38;5;{random.randint(0, 255)}m'
            formatted_quote += f'{random_color}{DARK_ULTRAMARINE_BLUE_BG}{char}{RESET}'  # Apply random color and dark ultramarine blue background to '|'
        else:
            formatted_quote += f'{YELLOW}{DARK_ULTRAMARINE_BLUE_BG}{char}{RESET}'  # Apply yellow text color and dark ultramarine blue background to other characters

    return formatted_quote


# This function formats a quote by applying ANSI escape sequences for colors and formatting
def format_quote2(quote):
    # ANSI escape sequences for colors
    RESET = '\033[0m'  # Reset all text formatting
    BLACK_BG = '\033[40m'  # Set background color to black
    WHITE_BG = '\033[107m'  # Set background color to white
    NEON_GREEN = '\033[92m'  # Set text color to neon green
    BOLD = '\033[1m'  # Set text formatting to bold
    
    formatted_quote = ''  # Initialize an empty string to store the formatted quote
    for char in quote:  # Iterate over each character in the input quote
        if '\033' in char:  # If the character already has a color escape sequence
            if '\033[30m' in char or '\033[31m' in char or '\033[32m' in char or '\033[33m' in char or '\033[34m' in char or '\033[35m' in char or '\033[36m' in char or '\033[37m' in char:
                # If the color is dark (colors 30-37), use white background
                formatted_quote += f'{WHITE_BG}{BOLD}{char}{RESET}'  # Apply white background and bold formatting to the character
            else:
                # If the color is bright, use black background
                formatted_quote += f'{BLACK_BG}{BOLD}{char}{RESET}'  # Apply black background and bold formatting to the character
        else:
            formatted_quote += f'{BLACK_BG}{BOLD}{NEON_GREEN}{char}{RESET}'  # Apply black background, bold formatting, and neon green text color to the character
    
    return f'{BLACK_BG}{formatted_quote}{RESET}'  # Apply black background to the entire formatted quote

program_title = "Visualizing Complex Roots of Quadratic Equations                             "
name = "Riki Hernandez                                         "


def startbanner():
    #source:
    banner = r'''
      ` : | | | |:  ||  :     `  :  |  |+|: | : : :|   .        `              .         
      ` : | :|  ||  |:  :    `  |  | :| : | : |:   |  .                    :             
         .' ':  ||  |:  |  '       ` || | : | |: : |   .  `           .   :.             
                `'  ||  |  ' |   *    ` : | | :| |*|  :   :               :|             
        *    *       `  |  : :  |  .      ` ' :| | :| . : :         *   :.||             
             .`            | |  |  : .:|       ` | || | : |: |          | ||             
      '          .         + `  |  :  .: .         '| | : :| :    .   |:| ||             
         .                 .    ` *|  || :       `    | | :| | :      |:| |              
 .                .          .        || |.: *          | || : :     :|||                
        .            .   . *    .   .  ` |||.  +        + '| |||  .  ||`                 
     .             *              .     +:`|!             . ||||  :.||`                  
 +                      .                ..!|*          . | :`||+ |||`                   
     .                         +      : |||`        .| :| | | |.| ||`       .            
       *     +   '               +  :|| |`     :.+. || || | |:`|| `                      
                            .      .||` .    ..|| | |: '` `| | |`  +                     
  .       +++                      ||        !|!: `       :| |                           
              +         .      .    | .      `|||.:      .||    .       .    `           
          '                           `|. + .  `:|||   + ||'     `                       
  __    +      *                         `A_      `'|.    `:                             
"'  `---"""----....                      /\-\         `.    `.  .    ____,.,-            
    ___,--'""`---"'  ~~~”’_             _||"|_          .___ __,..---""'                 
--"'                        “~~~—    ^~^~^~^~^   ——``--..,_        ` '                   
'''
    print(format_quote(banner))
    print(format_quote2(program_title))
    print(format_quote2(name))
    print("")

def print_int_array_with_colors(intArray, color_of_coefficient):

    colored_elements = []  # Initialize an empty list to store colored elements

    # Iterate over each element in intArray
    for i in intArray:
        color = color_of_coefficient[i]  # Get the color associated with the current element
        # Extract the RGB values from the color and create an ANSI escape sequence
        color_code = f"\033[38;2;{int(color[1:3], 16)};{int(color[3:5], 16)};{int(color[5:], 16)}m"
        # Create a colored element by combining the color escape sequence and the current element
        colored_element = f"{color_code}{i}\033[0m"
        colored_elements.append(colored_element)  # Add the colored element to the list

    colored_intArray = ", ".join(colored_elements)
    print("")
    print("You entered integer range:")
    print("")
    print(f"    [ {colored_intArray} ]")  


def plot_roots(permutations):
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d', facecolor='grey')
    ax2 = fig.add_subplot(122, facecolor='grey')
    ax2.grid(True)  # Add grid to the subplot

    real_roots = []
    complex_roots = []
    for i, (a, b, c) in enumerate(permutations):
        root1, root2 = quadratic_roots(a, b, c)
        if isinstance(root1, complex) or isinstance(root2, complex):
            complex_roots.append((root1, i+1))
            complex_roots.append((root2, i+1))
        else:
            real_roots.append((root1, i+1))
            real_roots.append((root2, i+1))

    real_roots = np.array(real_roots)
    complex_roots = np.array(complex_roots)

    def update_plot():
        ax1.clear()
        ax1.scatter(real_roots[:, 0], np.zeros_like(real_roots[:, 0]), 0, color='lime', label='Real Roots')
        ax1.scatter(complex_roots[:, 0].real, complex_roots[:, 0].imag, 0, color='orange', label='Complex Roots')
        ax1.set_xlabel('Real x axis', color='white')
        ax1.set_zlabel('Real y axis', color='white')
        ax1.set_ylabel('Imaginary axis', color='white')
        ax1.legend(facecolor='Gray', edgecolor='white', labelcolor='white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.tick_params(axis='z', colors='white')
        ax1.xaxis.set_pane_color((0, 0, 0, 1.0))
        ax1.yaxis.set_pane_color((0, 0, 0, 1.0))
        ax1.zaxis.set_pane_color((0, 0, 0, 1.0))

    update_plot()

    ax2.scatter(real_roots[:, 0], np.zeros_like(real_roots[:, 0]), color='lime', label='Real Roots')
    ax2.scatter(complex_roots[:, 0].real, complex_roots[:, 0].imag, color='orange', label='Complex Roots')
    ax2.set_xlabel('Real x axis', color='white')
    ax2.set_ylabel('Imaginary axis', color='white')
    ax2.legend(facecolor='black', edgecolor='white', labelcolor='white')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    equation_labels = {i+1: f'Eq#{i+1}' for i in range(len(permutations))}
    annotations = {}

    def on_hover(event):
        #source: https://stackoverflow.com/questions/10374930/matplotlib-annotating-a-3d-scatter-plot
        if event.inaxes == ax1:
            closestIndex = calcClosestDatapoint(np.concatenate((real_roots, complex_roots)), event, ax1)
            annotatePlot(np.concatenate((real_roots, complex_roots)), closestIndex, ax1, equation_labels)
        elif event.inaxes == ax2:
            closestIndex = calcClosestDatapoint2D(np.concatenate((real_roots, complex_roots)), event)
            annotatePlot2D(np.concatenate((real_roots, complex_roots)), closestIndex, ax2, equation_labels)

    def distance(point, event, ax):
        """Return distance between mouse position and given data point"""

        # Check if the shape of the point is (3,), raise an AssertionError if not
        assert point.shape == (3,), "distance: point.shape is wrong: %s, must be (3,)" % point.shape

        # Project the 3D point onto the 2D plane of the plot
        x2, y2, _ = proj3d.proj_transform(point[0], point[1], point[2], ax.get_proj())

        # Transform the projected 2D point to the coordinate system of the plot
        x3, y3 = ax.transData.transform((x2, y2))

        # Calculate the Euclidean distance between the transformed point and the mouse position
        return np.sqrt((x3 - event.x)**2 + (y3 - event.y)**2)



    # Calculate which data point is closest to the mouse position in 3D
    def calcClosestDatapoint(points, event, ax):
        distances = [distance(np.array([point[0].real, point[0].imag, 0]), event, ax) for point in points]
        return np.argmin(distances)

    # Return distance between mouse position and given data point in 2D
    def distance2D(point, event):
        x, y = point[0].real, point[0].imag
        return np.sqrt((x - event.xdata)**2 + (y - event.ydata)**2)

    # Calculate which data point is closest to the mouse position in 2D
    def calcClosestDatapoint2D(points, event):
        distances = [distance2D(point, event) for point in points]
        return np.argmin(distances)

    # Create popover label in 3D chart
    def annotatePlot(points, index, ax, equation_labels):
        if hasattr(annotatePlot, 'label'):
            annotatePlot.label.remove()  # Remove the existing label if it exists
        root = points[index][0]  # Get the root of the selected point
        x2, y2, _ = proj3d.proj_transform(root.real, root.imag, 0, ax.get_proj())  # Transform the root coordinates to 2D
        annotatePlot.label = ax.annotate(  # Create a new annotation label
            # Annotate the plot in 2D with a label
            equation_labels[points[index][1]],  # Get the equation label based on the index
            xy=(x2, y2),  # Set the position of the annotation
            xytext=(-20, 20),  # Set the offset of the text from the annotation position
            textcoords='offset points',  # Set the coordinate system for the text offset
            ha='right',  # Set the horizontal alignment of the text
            va='bottom',  # Set the vertical alignment of the text
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),  # Set the style and color of the annotation box
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')  # Set the style of the arrow connecting the annotation to the point
            )
        fig.canvas.draw()

    # Create popover label in 2D chart
    def annotatePlot2D(points, index, ax, equation_labels):

        # Check if the 'annotatePlot2D' function has the attribute 'label'
        if hasattr(annotatePlot2D, 'label'):
            # Remove the existing label if it exists
            annotatePlot2D.label.remove()

        # Get the root of the selected point from the 'points' array
        root = points[index][0]

        # Create a new annotation label for the selected point
        annotatePlot2D.label = ax.annotate(
            # Annotate the plot in 2D with a label
            equation_labels[points[index][1]],  # Get the equation label based on the index
            xy=(root.real, root.imag),  # Set the position of the annotation
            xytext=(-20, 20),  # Set the offset of the text from the annotation position
            textcoords='offset points',  # Set the coordinate system for the text offset
            ha='right',  # Set the horizontal alignment of the text
            va='bottom',  # Set the vertical alignment of the text
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),  # Set the style and color of the annotation box
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')  # Set the style of the arrow connecting the annotation to the point
        )


        fig.canvas.draw()

    fig.canvas.mpl_connect('motion_notify_event', on_hover)

    parabolas_visible = False

    def plot_parabolas(event):

        # Declare that the variable 'parabolas_visible' is nonlocal, meaning it refers to the same variable in the outer scope
        nonlocal parabolas_visible

        # Check if the parabolas are not currently visible
        if not parabolas_visible:
            # Generate x values from -10 to 10 with 100 points
            x = np.linspace(-10, 10, 100)

            # Iterate over the permutations of coefficients (a, b, c) in the 'permutations' list
            for i, (a, b, c) in enumerate(permutations):
                # Calculate the y values for the quadratic equation using the current coefficients
                y = a*x**2 + b*x + c

                # Set the color of the plotted line based on the index of the permutation
                color = 'lime' if i < len(real_roots) // 2 else 'orange'

                # Plot the quadratic curve on the chart with the x values and corresponding y values
                ax1.plot(x, np.zeros_like(x), y, color=color, alpha=0.5)

            # Set the variable 'parabolas_visible' to True to indicate that the parabolas are now visible
            parabolas_visible = True
        else:
            # Call the 'update_plot' function to update the chart without the parabolas
            update_plot()

            # Set the variable 'parabolas_visible' to False to indicate that the parabolas are no longer visible
            parabolas_visible = False

        plt.draw()
    # Create an axes object for the first button at the specified position and with the specified size and background color
    ax_button1 = plt.axes([0.7, 0.01, 0.1, 0.06])

    # Create a button object with the specified label, color, and hover color
    button1 = Button(ax_button1, 'Toggle Parabolas', color='white', hovercolor='gray')

    # Set the color of the button label to black
    button1.label.set_color('black')

    # Set the callback function for the button click event to the 'plot_parabolas' function
    button1.on_clicked(plot_parabolas)

    # Create an axes object for the second button at the specified position and with the specified size and background color
    ax_button2 = plt.axes([0.81, 0.01, 0.1, 0.06])

    # Create a button object with the specified label, color, and hover color
    button2 = Button(ax_button2, 'Toggle Rotation', color='white', hovercolor='gray')

    # Set the color of the button label to black
    button2.label.set_color('black')

    def rotate_plot():
        ax1.view_init(elev=30, azim=0)
        plt.draw()

    rotation_enabled = False

    def toggle_rotation(event):#VERY BUGGY NOT WORKING but breaks if removed
        nonlocal rotation_enabled
        if rotation_enabled:
            button2.label.set_text('Resume Rotation')
            rotation_enabled = False
        else:
            button2.label.set_text('Pause Rotation')
            rotation_enabled = True
            rotate_plot()

    button2.on_clicked(toggle_rotation)

    plt.tight_layout()
    plt.show()
    
def print_equations_and_roots(permutations, color_of_coefficient):
    """
    Prints the equations and their roots.
    
    Args:
        permutations (list): List of tuples representing the coefficients of the quadratic equations.
        color_of_coefficient (dict): Dictionary mapping coefficients to color codes.
    """
    equation_labels = {}
    max_equation_length = 0

    # Find the maximum length of the colored equations
    for a, b, c in permutations:
        # loop for formatting the quadratic equations with colored coefficients.
        # The color_of_coefficient dictionary maps each coefficient to a color code.
        # Then used to create ANSI escape sequences for colors.
        # The color coefficients a, b, and c are extracted from the color_of_coefficient
        # The extracted color codes then used to create ANSI escape sequences for colors.
        # The colored_equation string is created by combining the color codes with the corresponding coefficients.
        # The equation_length is calculated by removing the ANSI escape sequences from the colored_equation string.
        # These lines of code ensure that the quadratic equations are formatted with colored coefficients and
        # the length of the equations is calculated accurately for proper alignment.
        a_color = color_of_coefficient[a]
        b_color = color_of_coefficient[b]
        c_color = color_of_coefficient[c]

        a_color_code = f"\033[38;2;{int(a_color[1:3], 16)};{int(a_color[3:5], 16)};{int(a_color[5:], 16)}m"
        b_color_code = f"\033[38;2;{int(b_color[1:3], 16)};{int(b_color[3:5], 16)};{int(b_color[5:], 16)}m"
        c_color_code = f"\033[38;2;{int(c_color[1:3], 16)};{int(c_color[3:5], 16)};{int(c_color[5:], 16)}m"

        colored_equation = f"{a_color_code}{a}\033[0mx^2 + {b_color_code}{b}\033[0mx + {c_color_code}{c}\033[0m"
        equation_length = len(re.sub(r'\033\[[0-9;]*m', '', colored_equation))
        max_equation_length = max(max_equation_length, equation_length)

    # Iterate over the permutations and print the equations and roots
    for i, (a, b, c) in enumerate(permutations):

        d = (b**2) - (4*a*c)
        sol1 = (-b-cmath.sqrt(d))/(2*a)
        sol2 = (-b+cmath.sqrt(d))/(2*a)

        sol1_sci = f"{sol1:.2f}"
        sol2_sci = f"{sol2:.2f}"

        equation_labels[sol1_sci] = f'Eq#{i+1}'
        equation_labels[sol2_sci] = f'Eq#{i+1}'

        is_complex = (isinstance(sol1, complex) and sol1.imag != 0) or (isinstance(sol2, complex) and sol2.imag != 0)

        equation_padding = ' ' * (max_equation_length - equation_length)
        # This block of code prints the equations and their roots with proper formatting and color coding.
        # It iterates over the permutations of coefficients and calculates the roots of each equation.
        # Then, it prints the equation number, colored equation, roots, and whether the equation has complex roots.

        print(f'Eq #{i+1:2}: {colored_equation}{equation_padding}  \033[0mhas roots: ({sol1_sci:>10}) and ({sol2_sci:>10}); ' + ('Has complex roots: {}'.format('\033[92mTrue\033[0m' if is_complex else '\033[91mFalse\033[0m')))
        # The above line uses f-string formatto include equation number (i+1), colored equation, equation padding, roots (sol1_sci and sol2_sci),
        # and the result of the ternary operator that checks if the equation has complex roots.
        # The ternary operator formats output with color codes: ('\033[92mTrue\033[0m' for True and '\033[91mFalse\033[0m' for False).
      

    return equation_labels




# Main program
startbanner()

coefficients, color_of_coefficient = get_coefficients()
print_int_array_with_colors(coefficients, color_of_coefficient)
coefficientarray = find_unique_3_tuples(coefficients)
permutations = find_permutations(coefficientarray)

while True:
    choice = menu_options()

    if choice == '1':
        coefficients, color_of_coefficient = get_coefficients()
        print_int_array_with_colors(coefficients, color_of_coefficient)
        coefficientarray = find_unique_3_tuples(coefficients)
        permutations = find_permutations(coefficientarray)
    elif choice == '2':
        print("All quadratic equations from the permutations of the set of distinct coefficients a, b, c, generated by the input range of integers:")
        print_equations_and_roots(permutations, color_of_coefficient)
    elif choice == '3':
        coefficientarray = find_unique_3_tuples(coefficients)
        permutations = find_permutations(coefficientarray)
        plot_roots(permutations)
        input(">>Press Enter to continue...")
    elif choice == '4':
        # ANSI escape sequence to clear the terminal
        clear_terminal = "\033c"
        # Restart the Python file
        os.system("python " + __file__)
        # Clear the terminal
        print(clear_terminal)
    else:
        print("Invalid choice.")



#unworking code
        
   # ani = Animation.FuncAnimation(ax1, update_rotation, frames=360, interval=50, blit=False)

#   def toggle_rotation(event):
#     if ani.running:
#        ani.event_source.stop()
#   else:
#      ani.event_source.start()

#   ax_button_rotate = plt.axes([0.7, 0.07, 0.2, 0.06], facecolor='black')
#   button_rotate = Button(ax_button_rotate, 'Toggle Rotation', color='white', hovercolor='gray')
#   button_rotate.label.set_color('black')
#   button_rotate.on_clicked(toggle_rotation)
#
#   def update_rotation(num):
#       ax1.view_init(elev=10., azim=num)

#    def toggle_rotation(event):
#    if ani.event_source.timer is not None:
#       ani.pause()
#        button2.label.set_text('Resume Rotation')
#    else:
#        ani.resume()
#        button2.label.set_text('Pause Rotation')

#    button2.on_clicked(toggle_rotation)
        
# if event.inaxes == ax1 or event.inaxes == ax2:
            # for root, eq_num in np.concatenate((real_roots, complex_roots)):
            #     if event.inaxes == ax1:
            #         if np.abs(event.xdata - root.real) < 0.1 and np.abs(event.ydata - root.imag) < 0.1:
            #             if eq_num not in annotations:
            #                 annotations[eq_num] = event.inaxes.annotate(
        
            #                     equation_labels[eq_num],
            #                     xy=(root.real, root.imag),
            #                     xytext=(10, 10),
            #                     textcoords='offset points',
            #                     color='white',
            #                     ha='left',
            #                     va='bottom',
            #                     bbox=dict(boxstyle='round,pad=0.5', fc='black', ec='white', alpha=0.7),
            #                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='white')
            #                 )
            #             else:
            #                 annotations[eq_num].set_visible(True)
            #             fig.canvas.draw_idle()
            #             return
            #     elif event.inaxes == ax2:
            #         if np.abs(event.xdata - root.real) < 0.1 and np.abs(event.ydata - root.imag) < 0.1:
            #             if eq_num not in annotations:
            #                 annotations[eq_num] = event.inaxes.annotate(
            #                     equation_labels[eq_num],
            #                     xy=(root.real, root.imag),
            #                     xytext=(10, 10),
            #                     textcoords='offset points',
            #                     color='white',
            #                     ha='left',
            #                     va='bottom',
            #                     bbox=dict(boxstyle='round,pad=0.5', fc='black', ec='white', alpha=0.7),
            #                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='white')
            #                 )
            #             else:
            #                 annotations[eq_num].set_visible(True)
            #             fig.canvas.draw_idle()
            #             return



            # for eq_num in annotations:
            #     annotations[eq_num].set_visible(False)
            # fig.canvas.draw_idle()
 