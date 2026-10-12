#!/usr/bin/env python3
"""
Minecraft Stronghold Triangulation Calculator — Streamlit Web UI
"""

import streamlit as st
import math
from calculator import calculate_direction_vector, calculate_intersection, calculate_distance

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stronghold Triangulator",
    page_icon="🏰",
    layout="centered",
)

# ── Custom CSS for a Minecraft-y feel ────────────────────────────────────────
st.markdown("""
<style>
    .main .block-container {
        max-width: 650px;
        padding-top: 2rem;
    }
    .result-box {
        background-color: #1a1a2e;
        border: 2px solid #e94560;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
        color: #eee;
    }
    .coord-display {
        font-size: 1.8rem;
        font-weight: bold;
        color: #e94560;
        text-align: center;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #3d2b1f;
        border: 2px solid #f5a623;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        color: #ffd700;
    }
    .guide-box {
        background-color: #0f3460;
        border: 2px solid #16c79a;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1rem;
        color: #e0e0e0;
    }
    .guide-box h3 {
        color: #16c79a;
        margin-top: 0;
    }
    .step-badge {
        display: inline-block;
        background-color: #e94560;
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        text-align: center;
        line-height: 28px;
        font-weight: bold;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 🏰 Stronghold Triangulator")
st.markdown("Estimate your stronghold location using two Eye of Ender throws.")

# ── Step 1: Throw 1 ─────────────────────────────────────────────────────────
st.markdown("### <span class='step-badge'>1</span> Throw 1 — Stand at your position and throw an Eye of Ender", unsafe_allow_html=True)
st.markdown("Face the direction the eye flies toward, then press F3 and record your coordinates + yaw.")

x1 = st.number_input("X coordinate", value=0.0, format="%.1f", key="x1")
z1 = st.number_input("Z coordinate", value=0.0, format="%.1f", key="z1")
yaw1 = st.number_input("Yaw angle (°)", value=0.0, format="%.1f", key="yaw1",
                       help="Press F3 in Minecraft — the value after 'XYZ'")

# ── Step 2: Guidance for Throw 2 ────────────────────────────────────────────
st.markdown("---")
st.markdown("### <span class='step-badge'>2</span> Positioning for Throw 2", unsafe_allow_html=True)

# Calculate throw 1 direction to give guidance
dx1, dz1 = calculate_direction_vector(yaw1)
throw1_angle_deg = math.degrees(math.atan2(dx1, dz1))

# Perpendicular directions (±90° from throw 1 direction)
perp_a = throw1_angle_deg + 90
perp_b = throw1_angle_deg - 90

# Normalize to -180..180 range
def normalize_angle(a):
    while a > 180:
        a -= 360
    while a < -180:
        a += 360
    return a

perp_a_norm = normalize_angle(perp_a)
perp_b_norm = normalize_angle(perp_b)

st.markdown(f"""
<div class="guide-box">
<h3>🧭 Where to go for Throw 2</h3>
<p><strong>Goal:</strong> Move <strong>perpendicular</strong> (at a right angle) to your Throw 1 direction. This gives the most accurate triangulation.</p>

<p><strong>Your Throw 1 is heading roughly:</strong> {throw1_angle_deg:.0f}°</p>

<p><strong>For Throw 2, face one of these directions:</strong></p>
<ul>
<li>🧭 <strong>{perp_a_norm:.0f}°</strong> (turn left ~90° from throw 1)</li>
<li>🧭 <strong>{perp_b_norm:.0f}°</strong> (turn right ~90° from throw 1)</li>
</ul>

<p><strong>Distance:</strong> Move at least <strong>100 blocks</strong> away from Throw 1. More distance = better accuracy.<br>
Ideal range: <strong>100–500 blocks</strong>. The key is the perpendicular angle, not just distance.</p>

<p><strong>Quick tip:</strong> Pick whichever perpendicular direction is easier to reach — mountains, rivers, etc. Just make sure you're roughly at a right angle from your first throw line.</p>
</div>
""", unsafe_allow_html=True)

# ── Step 3: Throw 2 ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### <span class='step-badge'>3</span> Throw 2 — From your new position, throw another Eye of Ender", unsafe_allow_html=True)
st.markdown("Face the direction the eye flies toward (should be roughly perpendicular to throw 1), then press F3.")

x2 = st.number_input("X coordinate", value=100.0, format="%.1f", key="x2")
z2 = st.number_input("Z coordinate", value=100.0, format="%.1f", key="z2")
yaw2 = st.number_input("Yaw angle (°)", value=0.0, format="%.1f", key="yaw2",
                       help="Face the direction the eye flies, then read F3 yaw")

# ── Step 4: Calculate ───────────────────────────────────────────────────────
st.markdown("---")

if st.button("⚔️ Calculate Stronghold Location", type="primary", use_container_width=True):
    # Direction vectors
    dx1, dz1 = calculate_direction_vector(yaw1)
    dx2, dz2 = calculate_direction_vector(yaw2)

    # Intersection
    result = calculate_intersection(x1, z1, dx1, dz1, x2, z2, dx2, dz2)

    if len(result) == 3 and isinstance(result[2], str):
        st.error(f"❌ {result[2]}. The triangulation is unreliable — check your measurements.")
    else:
        ix, iz, t, s = result

        # Distances
        dist1 = calculate_distance(x1, z1, ix, iz)
        dist2 = calculate_distance(x2, z2, ix, iz)

        # Warnings
        warnings = []
        if t < 0:
            warnings.append("Throw 1: intersection is behind the throw direction")
        if s < 0:
            warnings.append("Throw 2: intersection is behind the throw direction")

        # ── Results ──────────────────────────────────────────────────────
        st.markdown("### 📍 Estimated Stronghold Location")

        st.markdown(f'<div class="coord-display">X: {ix:.0f} &nbsp;&nbsp; Z: {iz:.0f}</div>',
                    unsafe_allow_html=True)

        st.markdown(f"**Rounded block coordinate:** `{round(ix)}, {round(iz)}`")

        st.markdown(f"- Distance from Throw 1: **{dist1:.1f}** blocks")
        st.markdown(f"- Distance from Throw 2: **{dist2:.1f}** blocks")

        if warnings:
            st.markdown("")
            warn_text = "\n".join(f"⚠️ {w}" for w in warnings)
            st.warning(f"{warn_text}\nOne or both yaw measurements may be incorrect.")

        st.info(
            "This is an **estimated** location. Eye of Ender yaw has limited precision "
            "and points toward the stronghold's target chunk area, not the exact portal."
        )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Minecraft Stronghold Triangulation Calculator • Perpendicular throws = best accuracy")
