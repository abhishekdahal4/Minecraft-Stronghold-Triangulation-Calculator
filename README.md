# Minecraft Stronghold Triangulation Calculator

A precise, math-driven utility designed to calculate exact *Minecraft* stronghold coordinates using dual Eye of Ender throws. By modeling player orientation angles as 2D vector rays, this tool solves a system of linear equations via **Cramer's rule** to pinpoint structures with sub-block accuracy.

---

## Features
- **Parametric Vector Intersections:** Converts Minecraft Java Edition yaw angles into horizontal direction vectors and computes accurate ray intersections.
- **Robust Error Handling:** Detects parallel or near-parallel throws (preventing division-by-zero errors via determinant checks).
- **Trajectory Validation:** Flags anomalies where the computed intersection lies *behind* one or both throw positions ($t < 0$ or $s < 0$).
- **Dual Output Formats:** Provides continuous floating-point coordinates alongside rounded integer block coordinates for excavation.

---

## Mathematics Overview

1. **Yaw to Vector Conversion:**
   Minecraft yaw angles $\theta$ are converted to radians and projected onto the $XZ$-plane:
   $$dx = -\sin(\theta_{\text{rad}}), \quad dz = \cos(\theta_{\text{rad}})$$

2. **Parametric Line Equations:**
   Each throw defines a ray starting at $P(x, z)$ with direction vector $D(dx, dz)$:
   $$\mathbf{P}(t) = \mathbf{P}_1 + t \mathbf{D}_1$$

3. **Solving via Cramer's Rule:**
   Setting two throw rays equal to each other yields a $2 \times 2$ linear system solved efficiently using determinants.

For a deep-dive breakdown of the vector kinematics, check out the full [Technical Paper (PAPER.md)](./PAPER.md). (coming soon)

---

## Project Structure
```text
minecraft-stronghold-calculator/
│
├── calculator.py       # Core logic
├── calculator_web.py   # Web Interface
└── README.md           # Project documentation
```

---

## Getting Started (Command Line Interface)

### Prerequisites
- Python 3.6 or higher

### Installation & Execution
Clone the repository and run the script locally:
```bash
git clone https://github.com/your-username/minecraft-stronghold-calculator.git
cd minecraft-stronghold-calculator
python3 calculator.py
```

### Usage Example
When prompted, enter your coordinates and the yaw angle displayed in your debug screen (`F3`):
```text
============================================================
Minecraft Stronghold Triangulation Calculator
============================================================

------------------------------------------------------------
THROW 1
------------------------------------------------------------
X coordinate: 100
Z coordinate: -250
Yaw angle: 45

------------------------------------------------------------
THROW 2
------------------------------------------------------------
X coordinate: 320
Z coordinate: -100
Yaw angle: -30
```

---

## Author
**Abhishek Dahal**  
Cullen College of Engineering, University of Houston
