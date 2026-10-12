#!/usr/bin/env python3
"""
Minecraft Stronghold Triangulation Calculator
Calculates estimated stronghold coordinates using two Eye of Ender throws.
Author: Abhishek Dahal
"""

import math
from typing import Tuple, Optional, Union


def get_float_input(prompt: str) -> Optional[float]:
    """Get a float from user with validation, supporting 'q' to quit."""
    while True:
        try:
            value = input(prompt).strip()
            if value.lower() == 'q':
                return None
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a valid number or 'q' to quit.")


def calculate_direction_vector(yaw_degrees: float) -> Tuple[float, float]:
    """
    Convert Minecraft yaw angle to a 2D horizontal direction vector.
    
    Minecraft Java Edition yaw conventions:
    - 0° = South (+Z)
    - 90° = West (-X)
    - -90° = East (+X)
    - ±180° = North (-Z)
    """
    yaw_radians = math.radians(yaw_degrees)
    dx = -math.sin(yaw_radians)
    dz = math.cos(yaw_radians)
    return dx, dz


def calculate_intersection(
    x1: float, z1: float, dx1: float, dz1: float,
    x2: float, z2: float, dx2: float, dz2: float
) -> Union[Tuple[float, float, float, float], Tuple[None, None, str]]:
    """
    Calculate the intersection of two 2D parametric rays using Cramer's rule.
    Returns (ix, iz, t, s) on success or (None, None, error_message) on failure.
    """
    det = dx1 * (-dz2) - (-dx2) * dz1
    
    # Check for parallel or nearly parallel lines
    if abs(det) < 1e-6:
        return None, None, "Lines are parallel or nearly parallel"
    
    t = ((x2 - x1) * (-dz2) - (-dx2) * (z2 - z1)) / det
    s = (dx1 * (z2 - z1) - dz1 * (x2 - x1)) / det
    
    ix = x1 + t * dx1
    iz = z1 + t * dz1
    
    return ix, iz, t, s


def calculate_distance(x1: float, z1: float, x2: float, z2: float) -> float:
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((x2 - x1)**2 + (z2 - z1)**2)


def run_cli_session() -> None:
    """Run an interactive command-line session for the calculator."""
    print("=" * 60)
    print("Minecraft Stronghold Triangulation Calculator")
    print("=" * 60)
    print("\nThis tool estimates stronghold location using two Eye of")
    print("Ender throws. Type 'q' at any prompt to exit.\n")
    
    while True:
        print("-" * 60)
        print("THROW 1")
        print("-" * 60)
        x1 = get_float_input("X coordinate: ")
        if x1 is None:
            break
        z1 = get_float_input("Z coordinate: ")
        if z1 is None:
            break
        yaw1 = get_float_input("Yaw angle: ")
        if yaw1 is None:
            break
        
        print("\n" + "-" * 60)
        print("THROW 2")
        print("-" * 60)
        x2 = get_float_input("X coordinate: ")
        if x2 is None:
            break
        z2 = get_float_input("Z coordinate: ")
        if z2 is None:
            break
        yaw2 = get_float_input("Yaw angle: ")
        if yaw2 is None:
            break
        
        # Compute direction vectors and intersection
        dx1, dz1 = calculate_direction_vector(yaw1)
        dx2, dz2 = calculate_direction_vector(yaw2)
        
        result = calculate_intersection(x1, z1, dx1, dz1, x2, z2, dx2, dz2)
        
        if result[0] is None:
            print(f"\nERROR: {result[2]}")
            print("The triangulation is unreliable. Please check your measurements.\n")
            continue
        
        ix, iz, t, s = result
        
        # Validate ray direction parameters
        warnings = []
        if t < 0:
            warnings.append("Throw 1: intersection is behind the throw direction")
        if s < 0:
            warnings.append("Throw 2: intersection is behind the throw direction")
        
        dist1 = calculate_distance(x1, z1, ix, iz)
        dist2 = calculate_distance(x2, z2, ix, iz)
        
        # Display results
        print("\n" + "=" * 60)
        print("Estimated Stronghold Location")
        print("=" * 60)
        print(f"X: {ix:.2f}")
        print(f"Z: {iz:.2f}\n")
        print(f"Rounded block coordinate: {round(ix)}, {round(iz)}\n")
        print(f"Distance from Throw 1: {dist1:.1f} blocks")
        print(f"Distance from Throw 2: {dist2:.1f} blocks")
        
        if warnings:
            print("\nWARNING:")
            for warning in warnings:
                print(f"  - {warning}")
            print("One or both yaw measurements may be incorrect.")
        
        print("\nNOTE: Estimated location points toward the stronghold target chunk.")
        print("=" * 60 + "\n")
        
        cont = input("Calculate another pair? (Enter to continue, 'q' to quit): ").strip().lower()
        if cont == 'q':
            break
        print()
    
    print("Goodbye!")


if __name__ == "__main__":
    run_cli_session()