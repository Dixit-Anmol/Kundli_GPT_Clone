# Kundli GPT — Vedic Astrology & Ayurvedic Platform

A Vedic Astrology web application combining Jyotish Vidya and Ayurvedic principles with an intelligent consultation engine. Kundli GPT provides birth chart calculations, interactive animated horoscope visualizations, multi-profile management, and domain-focused astrological consultation.

---

## Key Features

### 1. Interactive Animated North Indian Kundli Chart
- **Stroke-by-Stroke Line Drawing Animation**: Authentic visual creation of the D1 Janam Kundli chart through stroke animations.
- **Dynamic House & Sign Indexing**: Displays exact zodiac sign numbers (1–12) calculated from the Ascendant sign following the traditional North Indian counter-clockwise layout.
- **Centroid Planet Placement**: Every planet (*Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu*) is placed at its exact mathematical centroid with interactive hover tooltips (*degrees, house lords, nakshatras*).
- **Planetary Position Table**: Detailed breakdown of planetary positions, dignity status (*Exalted, Own, Debilitated*), and *Retrograde [R]* indicators.

### 2. Multi-Profile Family & Friend Management
- **Store Up to 5 Profiles**: Save and manage birth charts for yourself, family members, or friends in local browser storage.
- **Relationship Tagging**: Categorize profiles cleanly (*Self, Spouse, Child, Parent, Friend, Other*).
- **Dynamic Navbar Switcher**: Instantly switch active profiles across all tabs without re-entering birth details.

### 3. Specialized Domain Modules
Comprehensive astrological analysis organized into 6 core domain modules:

| Module | Core Insights & Capabilities |
| :--- | :--- |
| **Overview** | Complete birth chart summary, Lagna personality, Moon sign, Nakshatra, Mahadasha timing, and interactive SVG Kundli chart. |
| **Career** | 10th House Karma analysis, professional strengths, career yogas, and timing for career advancements. |
| **Marriage** | 7th House partnership indicators, spouse traits, Manglik status assessment, and relationship dynamics. |
| **Health** | 1st & 6th House vitality ratings, physical & mental wellbeing indicators, and immunity insights. |
| **Food & Diet** | Ayurvedic Prakriti estimation (**Vata**, **Pitta**, **Kapha** proportions) paired with personalized dietary guidance. |
| **Finance** | 2nd & 11th House wealth analysis, Dhana Yogas, investment tendencies, and favorable financial periods. |

### 4. Consultation Engine
- **Structured Overview Readings**: Comprehensive multi-section readings when opening any domain tab.
- **Focused Q&A Responses**: Follow-up chat queries provide concise, direct answers focused specifically on the user's question without repeating template headers.
- **Vedic Terminology**: Integrates traditional Sanskrit/Hindi names alongside standard astrological terms (*e.g., Scorpio (Vrishchik), Sun (Surya), Jupiter (Guru)*).

---

## Design System & Architecture

- **Color Palette**: Styled in Kesari (`#E67E22`) and Sandalwood Cream (`#FAF8F3`) with clean gold accents.
- **Typography**: Uses EB Garamond for headings and Inter for user interface text.
- **Responsive Layout**: Designed for seamless viewing across Desktop, Tablet, and Mobile devices.

---

## Local Development Setup

### Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10+)

### 1. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload
```
*Backend server runs at: `http://127.0.0.1:8000`*

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
*Frontend runs at: `http://localhost:5173`*

---

## Technical Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Material Symbols Icons, React Markdown.
- **Backend**: Python 3.10, FastAPI, Uvicorn, Pydantic.
- **Astrology Engine**: Custom Sidereal Lahiri Ayanamsha Ephemeris engine calculating planetary longitudes, house cusps, Nakshatras, and Ayurvedic Prakriti doshas.
