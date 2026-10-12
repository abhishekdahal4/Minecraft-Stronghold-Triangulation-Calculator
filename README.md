# Minecraft Stronghold Triangulation Calculator

Estimates stronghold coordinates in Minecraft Java Edition using two Eye of Ender throws.

## Setup & Run (Ubuntu)

No installation needed — uses only the Python standard library.

```bash
cd ~/minecraft-stronghold-calc
python3 stronghold.py
```

Or run directly:

```bash
./stronghold.py
```

## How to Use

For each of two throws, enter:
- **X** coordinate (from F3 debug screen)
- **Z** coordinate
- **Yaw** angle (from F3 debug screen, in degrees)

The program calculates where the two Eye of Ender direction lines intersect.

## How the Triangulation Math Works

Each Eye of Ender throw gives you a position (X, Z) and a yaw angle. The yaw defines a 2D direction vector:

```
dx = -sin(yaw)
dz =  cos(yaw)
```

This creates two infinite lines in the XZ plane:

```
Line 1: P = P1 + t * D1
Line 2: P = P2 + s * D2
```

Where P1, P2 are throw positions and D1, D2 are direction vectors.

At the intersection point, both lines equal the same (X, Z). This gives a 2x2 linear system:

```
t*dx1 - s*dx2 = x2 - x1
t*dz1 - s*dz2 = z2 - z1
```

Solved using Cramer's rule. The determinant tells us if lines are parallel (no unique intersection). The parameters t and s tell us if the intersection is in front of or behind each throw.

## Important Notes

- This gives an **estimated** location, not guaranteed exact portal coordinates
- Eye of Ender yaw has limited precision (roughly ±2-3 degrees)
- The Eye points toward the stronghold's target chunk area, not necessarily the exact End Portal
- For best results, make throws from far apart (>50 blocks) with significantly different angles

## Test Case

```
Throw 1: X=-1337, Z=223, Yaw=6.6
Throw 2: X=-1320, Z=224, Yaw=9.5

Result: X≈-1375, Z≈555
```
