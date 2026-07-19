# Kundli GPT — Advanced Vedic Astrology & Ayurvedic Consultation Platform

Kundli GPT is a comprehensive Vedic Astrology and Ayurvedic consultation platform designed to bridge ancient Indian knowledge systems with modern web technologies. By integrating sidereal astronomical computations with automated domain analysis, the platform provides personalized birth chart calculations, interactive Kundli visual representations, multi-profile management, and dedicated consultation modules across key life areas.

---

## Core System Features

### 1. Interactive North Indian Kundli Chart (D1 Lagna)
- **Stroke-by-Stroke Line Drawing**: Uses staggered SVG stroke animations to visually construct the traditional North Indian diamond-square chart grid upon rendering.
- **Dynamic House & Sign Mapping**: Computes exact zodiac sign numbers (1–12) for all 12 houses relative to the user's calculated Ascendant sign, following the counter-clockwise North Indian astrological layout.
- **Precise Centroid Placement**: Position calculation places every planet (*Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu*) at the exact mathematical center of its house diamond or triangle, preventing overlap with grid lines.
- **Interactive Tooltips**: Hovering over any house or planetary badge reveals detailed metadata including sign name, exact degrees, house lord, and Nakshatra placements.
- **Planetary Position Table (Graha Sthiti)**: A companion data grid providing complete planetary longitudes, house cusps, Nakshatra Padas, dignity classifications (*Exalted, Own Sign, Debilitated*), and *Retrograde [R]* or *Combust* status.

### 2. Multi-Profile Family & Friend Management
- **Local Storage Management**: Store up to 5 individual birth profiles directly in browser local storage without requiring account creation.
- **Relationship Categorization**: Tag profiles with relationship identifiers (*Self, Spouse, Child, Parent, Friend, Other*) for organized access.
- **Dynamic Navbar Switcher**: Switch between saved profiles from the top navigation bar to dynamically recompute and update all dashboard visualizations and domain readings.

### 3. Dedicated Astrological Domain Modules

#### Overview Module
Provides a complete high-level synthesis of the horoscope, featuring Lagna personality characteristics, Moon sign emotional traits, Nakshatra details, current Vimshottari Mahadasha timing, lucky colors, lucky numbers, and dominant elemental distributions alongside the interactive Kundli chart.

#### Career & Profession Module
Analyzes the 10th House (*Karma Bhava*), 6th House (*Service and Competition*), 2nd House (*Income*), and 11th House (*Gains*). Identifies professional strengths, active career Yogas (*such as Raj Yoga*), 10th lord dignity, and favorable Dasha timing for career transitions, business ventures, or promotions.

#### Marriage & Relationships Module
Focuses on the 7th House (*Kalatra Bhava*), Venus, Jupiter, and Darakaraka placements. Evaluates spouse traits, relationship dynamics, partnership compatibility, and Manglik Dosha status with clear explanations of its presence or absence.

#### Health & Wellness Module
Examines the 1st House (*Vitality*), 6th House (*Immunity and Resistance*), and 8th/12th House influences. Provides astrological estimations of bodily constitution, mental wellbeing, physical strengths, and potential vulnerable health areas.

#### Food & Diet (Ayurvedic Prakriti) Module
Combines astrological indicators to estimate the user's Ayurvedic constitution across the three doshas: Vata (*Air/Ether*), Pitta (*Fire/Water*), and Kapha (*Earth/Water*). Generates customized dietary guidance highlighting foods to favor, foods to limit, ideal meal timing, and balancing herbs.

#### Finance & Wealth Module
Evaluates the 2nd House (*Accumulated Wealth*), 5th House (*Investments*), 8th House (*Inheritance*), and 11th House (*Financial Gains*). Identifies active Dhana Yogas, investment tendencies, Jupiter Karakaships, and favorable timing for wealth accumulation.

### 4. Dual-Mode Consultation Engine
- **Structured Initial Readings**: When selecting any domain tab, the system provides a comprehensive, structured domain overview formatted with clear markdown sections and relevant metrics.
- **Direct & Focused Q&A Responses**: Follow-up chat queries generate concise, direct answers (100–180 words) tailored specifically to the user's exact question, omitting repetitive template headers to optimize clarity and context.
- **Authentic Terminology**: Integrates traditional Sanskrit and Hindi astrological terms alongside English translations (*e.g., Scorpio (Vrishchik), Sun (Surya), Jupiter (Guru), Tanu Bhava, Dhana Bhava*).

---

## Design & Architecture

- **Visual Palette**: Designed using Kesari (`#E67E22`) and Sandalwood Cream (`#FAF8F3`) with clean gold accents and subtle glassmorphic card elements.
- **Typography**: Features EB Garamond for classical headings and Inter for user interface text.
- **Responsive Layout**: Adapts cleanly across desktop monitors, tablets, and mobile screens.

---

## Technology Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Material Symbols Icons, React Markdown.
- **Backend**: Python 3.10, FastAPI, Uvicorn, Pydantic.
- **Astrological Computation Engine**: Custom Sidereal Lahiri Ayanamsha Ephemeris engine calculating planetary longitudes, house cusps, Nakshatras, Vimshottari Dashas, and Ayurvedic Prakriti dosha distributions.
