# 🕉️ Kundli GPT — AI-Powered Vedic Astrology & Ayurvedic Platform

A state-of-the-art Vedic Astrology web application combining ancient **Jyotish Vidya** and **Ayurvedic Wisdom** with advanced AI intelligence. Kundli GPT delivers precise birth chart calculations, interactive animated horoscope visualizations, multi-profile family management, and domain-focused AI consultation.

---

## ✨ Key Features

### 1. 📊 Interactive Animated North Indian Kundli Chart
- **Stroke-by-Stroke Line Drawing Animation**: Experience the authentic creation of your D1 Janam Kundli with smooth line-by-line drawing animations.
- **Dynamic House & Sign Indexing**: Displays exact zodiac sign numbers (1–12) calculated from your Ascendant sign following traditional North Indian counter-clockwise layout.
- **Centroid Planet Placement**: Every Graha (*Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu*) sits at its exact mathematical centroid with interactive hover tooltips (*degrees, house lords, nakshatras*).
- **Graha Sthiti Table**: Comprehensive planetary position breakdown with dignity status (*Exalted, Own, Debilitated*) and *Retrograde [R]* indicators.

### 2. 👨‍👩‍👧‍👦 Multi-Profile Family & Friend Management
- **Store Up to 5 Profiles**: Easily save and manage birth charts for yourself, family members, or friends in local browser storage.
- **Relationship Tags**: Label profiles cleanly (*Self, Spouse, Child, Parent, Friend, Other*).
- **Dynamic Navbar Switcher**: Instantly switch between saved profiles across all tabs without re-entering birth details.

### 3. 🎯 Specialized Domain Modules
Explore deep astrological insights categorized across 6 dedicated domain hubs:

| Module | Core Insights & Capabilities |
| :--- | :--- |
| **🌟 Overview** | Complete birth chart summary, Lagna personality, Moon sign, Nakshatra, Mahadasha timing, and interactive SVG Kundli chart. |
| **💼 Career** | 10th House Karma analysis, professional strengths, career yogas, and timing for career advancements. |
| **💍 Marriage** | 7th House partnership indicators, spouse traits, Manglik status assessment, and relationship dynamics. |
| **🏥 Health** | 1st & 6th House vitality ratings, physical & mental wellbeing indicators, and immunity insights. |
| **🍽️ Food & Diet** | Ayurvedic Prakriti estimation (**Vata**, **Pitta**, **Kapha** proportions) paired with personalized dietary guidance. |
| **💰 Finance** | 2nd & 11th House wealth analysis, Dhana Yogas, investment tendencies, and favorable financial periods. |

### 4. 🧠 Dual-Mode AI Consultation Engine
- **Structured Overview Readings**: Rich, multi-section initial readings when opening any domain tab.
- **Direct & Focused Q&A**: Follow-up chat queries yield concise, direct answers focused strictly on your specific question (100–180 words) without repeating unnecessary section headers.
- **Traditional Hindi Terminology**: Features authentic Sanskrit/Hindi names alongside standard terms (*e.g., Scorpio (Vrishchik), Sun (Surya), Jupiter (Guru)*).

---

## 🎨 Design System & Aesthetics

- **Palette**: Crafted in **Vedic Kesari (`#E67E22`)** and warm **Sandalwood Cream (`#FAF8F3`)** with subtle glassmorphism and gold accents.
- **Typography**: Paired Google Fonts — **EB Garamond** for classical headings and **Inter** for crisp UI body text.
- **Responsive**: Fully optimized for Desktop, Tablet, and Mobile viewing.

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10+)

### 1. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI backend server
uvicorn main:app --reload
```
*Backend runs at: `http://127.0.0.1:8000`*

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
*Frontend runs at: `http://localhost:5173`*

---

## 🛠️ Technology Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS v4, Lucide & Material Symbols Icons, React Markdown.
- **Backend**: Python 3.10, FastAPI, Uvicorn, Pydantic, HTTP client streaming.
- **Astrology Engine**: Custom Sidereal Lahiri Ayanamsha Ephemeris engine computing exact planetary longitudes, house cusps, Nakshatras, and Ayurvedic Prakriti doshas.
