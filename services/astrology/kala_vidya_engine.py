"""
Vedic Kala & Vidya Analysis Engine — Classical 64 Chatushashti Kalas in Devanagari.

Evaluates and ranks the 64 classical Vedic Kalas (Chatushashti Kala) from the user's birth chart
using planetary longitudes, house lords (2nd, 3rd, 4th, 5th, 9th, 10th, 11th), dignities, and divisional charts.
"""

from typing import Dict, Any, List

# Complete 64 Classical Kalas (Chatushashti Kala) in Devanagari with Astrological Mapping
CLASSICAL_64_KALAS = [
    {
        "name": "Gīta vidyā",
        "devanagari": "गीतविद्या",
        "meaning": "Singing & Vocal Music",
        "houses": [2, 3, 5],
        "planets": ["venus", "mercury", "moon"],
        "reason": "2nd house of speech and 3rd/5th house of artistic expression powered by Venus and Moon."
    },
    {
        "name": "Vādya vidyā",
        "devanagari": "वाद्यविद्या",
        "meaning": "Playing Musical Instruments",
        "houses": [3, 5],
        "planets": ["venus", "mercury", "mars"],
        "reason": "3rd house of hands and dexterity with Venus and Mercury instrument resonance."
    },
    {
        "name": "Nṛtya vidyā",
        "devanagari": "नृत्यविद्या",
        "meaning": "Dancing & Expressive Movement",
        "houses": [3, 5, 1],
        "planets": ["venus", "mars"],
        "reason": "3rd house physical agility and Venus grace with Mars rhythmic energy."
    },
    {
        "name": "Nāṭya vidyā",
        "devanagari": "नाट्यविद्या",
        "meaning": "Theatrical Performance & Acting",
        "houses": [3, 5, 10],
        "planets": ["venus", "rahu", "mercury"],
        "reason": "5th house drama and Rahu impressionism with Mercury versatility."
    },
    {
        "name": "Ālekhya vidyā",
        "devanagari": "आलेख्यविद्या",
        "meaning": "Painting & Fine Arts",
        "houses": [3, 4, 5],
        "planets": ["venus", "moon"],
        "reason": "3rd house fine hand skills and 4th/5th aesthetic imagination via Venus."
    },
    {
        "name": "Viśeṣaka-cchēdya vidyā",
        "devanagari": "विशेषकच्छेद्यविद्या",
        "meaning": "Body Decoration & Cosmetology",
        "houses": [1, 3],
        "planets": ["venus", "mercury"],
        "reason": "Venus aesthetic adornment and 1st house physical presentation."
    },
    {
        "name": "Tāṇḍula-kusuma-balivikāra",
        "devanagari": "ताण्डुलकुसुमबलिविकार",
        "meaning": "Preparing Sacred Offerings",
        "houses": [5, 9],
        "planets": ["jupiter", "sun"],
        "reason": "9th house of rituals and Jupiter spiritual devotion."
    },
    {
        "name": "Puṣpastaraṇa",
        "devanagari": "पुष्पास्तरण",
        "meaning": "Floral Bed & Spatial Design",
        "houses": [4, 12],
        "planets": ["venus", "moon"],
        "reason": "4th house comfort and 12th house luxury aesthetics."
    },
    {
        "name": "Danta-vasanāṅga-rāga",
        "devanagari": "दन्तवसनाङ्गराग",
        "meaning": "Perfumes & Cleansing Products",
        "houses": [2, 6],
        "planets": ["venus", "mercury"],
        "reason": "Venus aromatic essence and 6th house personal care."
    },
    {
        "name": "Maṇi-bhūmikā-karma",
        "devanagari": "मणिभूमिकाकर्म",
        "meaning": "Crafting Jewel Settings & Gemology",
        "houses": [2, 3, 11],
        "planets": ["sun", "venus", "mars"],
        "reason": "2nd house precious gems and Sun/Venus mineral precision."
    },
    {
        "name": "Śayyā-racana",
        "devanagari": "शय्यारचन",
        "meaning": "Arranging Bedding & Comfort Spaces",
        "houses": [4, 12],
        "planets": ["venus", "moon"],
        "reason": "12th house relaxation and Venus comfort aesthetics."
    },
    {
        "name": "Udaka-vādya",
        "devanagari": "उदकवाद्य",
        "meaning": "Acoustic Music with Water",
        "houses": [3, 4],
        "planets": ["moon", "venus"],
        "reason": "Moon water element resonance with 3rd house acoustic sound."
    },
    {
        "name": "Udaka-ghāta",
        "devanagari": "उदकघात",
        "meaning": "Water Hydraulics & Splashing Sports",
        "houses": [4, 5],
        "planets": ["moon", "mars"],
        "reason": "Moon fluid dynamics and Mars aquatic energy."
    },
    {
        "name": "Citra-yoga",
        "devanagari": "चित्रयोग",
        "meaning": "Pigment Chemistry & Color Formulation",
        "houses": [3, 5],
        "planets": ["mercury", "venus"],
        "reason": "Mercury chemistry logic and Venus color harmony."
    },
    {
        "name": "Mālya-grathana-vikalpa",
        "devanagari": "माल्यग्रथनविकल्प",
        "meaning": "Floral Garland Synthesis",
        "houses": [3, 5],
        "planets": ["venus", "mercury"],
        "reason": "Venus floral beauty and 3rd house hand weaving."
    },
    {
        "name": "Śekharāpīḍa-yojana",
        "devanagari": "शेखरापीडयोजन",
        "meaning": "Coronet & Crown Crafting",
        "houses": [1, 10],
        "planets": ["sun", "venus"],
        "reason": "Sun royal authority and Venus ornamental crafting."
    },
    {
        "name": "Nēpathyayoga",
        "devanagari": "नेपथ्ययोग",
        "meaning": "Costume & Fashion Design",
        "houses": [3, 10],
        "planets": ["venus", "rahu"],
        "reason": "Venus sartorial style and Rahu modern trendsetting."
    },
    {
        "name": "Karṇapātra-bhaṅga",
        "devanagari": "कर्णपत्रभङ्ग",
        "meaning": "Ear Ornament Carving",
        "houses": [3, 2],
        "planets": ["venus", "mercury"],
        "reason": "2nd house ears and Venus delicate carving."
    },
    {
        "name": "Sugandha-yukti",
        "devanagari": "सुगन्धयुक्ति",
        "meaning": "Perfumery & Fragrance Synthesis",
        "houses": [2, 5],
        "planets": ["venus", "jupiter"],
        "reason": "Venus aromatic chemistry and Jupiter formulation wisdom."
    },
    {
        "name": "Bhūṣaṇa-yojana",
        "devanagari": "भूषणयोजन",
        "meaning": "Ornamentation & Jewelry Styling",
        "houses": [2, 1],
        "planets": ["venus", "sun"],
        "reason": "2nd house family jewels and Sun radiance."
    },
    {
        "name": "Aindra-jāla",
        "devanagari": "ऐन्द्रजाल",
        "meaning": "Illusion, Magic & Sleight of Hand",
        "houses": [3, 5, 8],
        "planets": ["rahu", "mercury"],
        "reason": "Rahu illusionary magic and Mercury swift hand agility."
    },
    {
        "name": "Kaucumāra",
        "devanagari": "कौचुमार",
        "meaning": "Esoteric & Mystic Arts",
        "houses": [8, 12],
        "planets": ["ketu", "jupiter"],
        "reason": "8th house secret sciences and Ketu occult mastery."
    },
    {
        "name": "Hasta-lāghava",
        "devanagari": "हस्तलाघव",
        "meaning": "Manual Dexterity & Fine Mechanics",
        "houses": [3],
        "planets": ["mercury", "mars"],
        "reason": "3rd house precise motor skills and Mercury speed."
    },
    {
        "name": "Citra-śākā-pūpa-bhakṣya-vikāra-kriyā",
        "devanagari": "चित्रशाकापूपभक्ष्यविकारक्रिया",
        "meaning": "Culinary Arts & Gourmet Cooking",
        "houses": [2, 4],
        "planets": ["moon", "venus", "mars"],
        "reason": "2nd house taste and Moon culinary nourishment."
    },
    {
        "name": "Pānaka-rasa-rāgāsava-yojana",
        "devanagari": "पानकरसरागासवयोजन",
        "meaning": "Mixology & Beverage Crafting",
        "houses": [2, 5],
        "planets": ["moon", "venus"],
        "reason": "2nd house fluids and Moon/Venus taste formulation."
    },
    {
        "name": "Sūci-vāya-karma",
        "devanagari": "सूचिवायकर्म",
        "meaning": "Needlework, Embroidery & Weaving",
        "houses": [3],
        "planets": ["venus", "mercury"],
        "reason": "3rd house needle precision and Venus textile arts."
    },
    {
        "name": "Sūtra-kṛīḍā",
        "devanagari": "सूत्रक्रीडा",
        "meaning": "Puppetry & String Mechanics",
        "houses": [3, 5],
        "planets": ["mercury", "rahu"],
        "reason": "3rd house finger manipulation and Rahu entertainment."
    },
    {
        "name": "Vīṇā-ḍamaruka-vādya",
        "devanagari": "वीणाडमरुकवाद्य",
        "meaning": "String Instrument & Percussion Mastery",
        "houses": [3, 5],
        "planets": ["venus", "mars"],
        "reason": "Venus string melody and Mars percussion rhythm."
    },
    {
        "name": "Prahelikā",
        "devanagari": "प्रहेलिका",
        "meaning": "Riddle Solving & Puzzle Mechanics",
        "houses": [5],
        "planets": ["mercury", "ketu"],
        "reason": "5th house puzzle logic and Ketu analytical precision."
    },
    {
        "name": "Durvacaka-yoga",
        "devanagari": "दुर्वचकयोग",
        "meaning": "Linguistic Conundrums & Cryptography",
        "houses": [2, 5],
        "planets": ["mercury", "rahu"],
        "reason": "Mercury speech logic and Rahu code cracking."
    },
    {
        "name": "Pustaka-vācana",
        "devanagari": "पुस्तकवाचन",
        "meaning": "Literary Recitation & Book Reading",
        "houses": [2, 4, 5],
        "planets": ["mercury", "jupiter"],
        "reason": "4th/5th house learning and Mercury book recitation."
    },
    {
        "name": "Nāṭikā-khyāyikā-darśana",
        "devanagari": "नाटिकाख्यायिकादर्शन",
        "meaning": "Storytelling & Dramatic Enactment",
        "houses": [3, 5],
        "planets": ["mercury", "moon"],
        "reason": "3rd house narrative and Moon emotional portrayal."
    },
    {
        "name": "Kāvya-samasya-pūraṇa",
        "devanagari": "काव्यसमस्यापूरण",
        "meaning": "Poetic Verse Composition",
        "houses": [2, 5],
        "planets": ["venus", "jupiter", "mercury"],
        "reason": "5th house poetic genius and Venus/Jupiter prosody."
    },
    {
        "name": "Paṭṭikā-vetra-bāṇa-vikalpa",
        "devanagari": "पट्टिकावेत्रबाणविकल्प",
        "meaning": "Weapons, Armor & Shield Crafting",
        "houses": [3, 6],
        "planets": ["mars", "saturn"],
        "reason": "6th house combat and Mars weapons technology."
    },
    {
        "name": "Tarku-karma",
        "devanagari": "तर्कुकर्म",
        "meaning": "Spindle Spinning & Fiber Technology",
        "houses": [3],
        "planets": ["saturn", "mercury"],
        "reason": "3rd house spindle spinning and Saturn fiber crafts."
    },
    {
        "name": "Takṣaṇa",
        "devanagari": "तक्षण",
        "meaning": "Carpentry & Structural Woodwork",
        "houses": [4, 3],
        "planets": ["mars", "saturn"],
        "reason": "4th house structural wood and Mars/Saturn craft."
    },
    {
        "name": "Vāstu-vidyā",
        "devanagari": "वास्तुविद्या",
        "meaning": "Architecture & Structural Engineering",
        "houses": [4, 10],
        "planets": ["mars", "saturn", "venus"],
        "reason": "4th house land/buildings with Saturn architecture and Mars engineering."
    },
    {
        "name": "Raupya-ratna-parīkṣā",
        "devanagari": "रौप्यरत्नपरीक्षा",
        "meaning": "Testing Gems & Precious Metals",
        "houses": [2, 5, 11],
        "planets": ["sun", "mercury", "jupiter"],
        "reason": "2nd house gems and Mercury scientific verification."
    },
    {
        "name": "Dhātu-vāda",
        "devanagari": "धातुवाद",
        "meaning": "Metallurgy & Material Science",
        "houses": [3, 10],
        "planets": ["mars", "saturn"],
        "reason": "Mars metals and Saturn mineralurgy."
    },
    {
        "name": "Maṇi-rāga-jñāna",
        "devanagari": "मणिशरागज्ञान",
        "meaning": "Jewel Dyeing & Gem Coloration",
        "houses": [2, 5],
        "planets": ["venus", "sun"],
        "reason": "Venus gemstone aesthetics and Sun clarity."
    },
    {
        "name": "Ākāra-jñāna",
        "devanagari": "आकारज्ञान",
        "meaning": "Mineralogy & Geology",
        "houses": [4, 8],
        "planets": ["saturn", "mars"],
        "reason": "4th/8th underground earth sciences and Saturn ore."
    },
    {
        "name": "Vṛkṣāyurveda-yoga",
        "devanagari": "वृक्षायुर्वेदयोग",
        "meaning": "Botany, Herbal Medicine & Plant Healing",
        "houses": [4, 6],
        "planets": ["mercury", "jupiter", "sun"],
        "reason": "4th house flora and Mercury/Jupiter botanical medicine."
    },
    {
        "name": "Meṣa-kukkuṭa-lāvaka-yuddha-vidhi",
        "devanagari": "मेषकुक्कुटलावकयुद्धविधि",
        "meaning": "Animal Behavior & Training Sciences",
        "houses": [6],
        "planets": ["mars", "saturn"],
        "reason": "6th house animals and Mars instinct control."
    },
    {
        "name": "Śuka-sārikā-pralāpana",
        "devanagari": "शुकसारिकाप्रलापन",
        "meaning": "Linguistic Avian Speech Training",
        "houses": [2, 3],
        "planets": ["mercury", "jupiter"],
        "reason": "2nd house vocal imitation and Mercury bird speech."
    },
    {
        "name": "Utsādana",
        "devanagari": "उत्सादन",
        "meaning": "Massage Therapy & Somatic Hygiene",
        "houses": [1, 6],
        "planets": ["mars", "venus"],
        "reason": "1st house body therapy and Venus touch."
    },
    {
        "name": "Keśa-mārjana-kauśala",
        "devanagari": "केशमार्जनकौशल",
        "meaning": "Trichology & Hair Care Artistry",
        "houses": [1, 3],
        "planets": ["venus", "mercury"],
        "reason": "Venus hair grooming aesthetics."
    },
    {
        "name": "Akṣara-muṣṭika-kathana",
        "devanagari": "अक्षरमुष्टिकाकथन",
        "meaning": "Sign Language & Gesture Communication",
        "houses": [3],
        "planets": ["mercury"],
        "reason": "3rd house hand sign transmission."
    },
    {
        "name": "Dhāraṇa-mātrikā",
        "devanagari": "धारणामात्रिका",
        "meaning": "Talismanic & Protective Bio-Shields",
        "houses": [5, 9],
        "planets": ["jupiter", "ketu"],
        "reason": "5th/9th sacred mantric protective yantras."
    },
    {
        "name": "Deśa-bhāṣā-jñāna",
        "devanagari": "देशभाषाज्ञान",
        "meaning": "Linguistics & Regional Dialects",
        "houses": [2, 3, 9],
        "planets": ["mercury", "jupiter"],
        "reason": "2nd/3rd house multilingual fluency and Jupiter polyglot."
    },
    {
        "name": "Nirmiti-jñāna",
        "devanagari": "निर्मितिज्ञान",
        "meaning": "Predictive Science & Omen Analysis",
        "houses": [5, 8, 9],
        "planets": ["jupiter", "ketu"],
        "reason": "5th/8th house intuitive foresight and Ketu divination."
    },
    {
        "name": "Yantra-mātrikā",
        "devanagari": "यन्त्रमात्रिका",
        "meaning": "Mechanics, Robotics & Systems Engineering",
        "houses": [3, 5, 10],
        "planets": ["saturn", "mars", "mercury", "rahu"],
        "reason": "3rd/5th house engineering logic with Saturn/Mars robotics."
    },
    {
        "name": "Mlecchita-kutarka-vikalpa",
        "devanagari": "म्लेच्छितकुतर्कविकल्प",
        "meaning": "Foreign Logic, Debating & Counter-Arguments",
        "houses": [3, 6, 9],
        "planets": ["mercury", "rahu"],
        "reason": "6th house debate and Rahu foreign philosophy."
    },
    {
        "name": "Saṁvācya",
        "devanagari": "संवाच्य",
        "meaning": "Oratory, Speech & Dynamic Dialogue",
        "houses": [2, 3, 10],
        "planets": ["mercury", "jupiter"],
        "reason": "2nd/3rd house commanding public discourse."
    },
    {
        "name": "Mānasi kāvya-kriyā",
        "devanagari": "मानसी काव्यक्रिया",
        "meaning": "Spontaneous Mental Poetic Composition",
        "houses": [5],
        "planets": ["venus", "moon", "jupiter"],
        "reason": "5th house rapid creative inspiration."
    },
    {
        "name": "Kriyā-vikalpa",
        "devanagari": "क्रियाविकल्प",
        "meaning": "Therapeutic Design & Medical Remedies",
        "houses": [5, 6, 9],
        "planets": ["jupiter", "sun"],
        "reason": "6th house healing remedies and Jupiter bio-formulations."
    },
    {
        "name": "Calitaka-yoga",
        "devanagari": "चलितकयोग",
        "meaning": "Sacred Shrine Architecture",
        "houses": [4, 9],
        "planets": ["jupiter", "saturn"],
        "reason": "9th house temples and Saturn sacred masonry."
    },
    {
        "name": "Abhidhāna-kośa-chanda-jñāna",
        "devanagari": "अभिधानकोशछन्दोज्ञान",
        "meaning": "Lexicography & Metric Prosody",
        "houses": [2, 5],
        "planets": ["mercury", "jupiter"],
        "reason": "2nd/5th house vocabulary and prosody."
    },
    {
        "name": "Vastra-gopana",
        "devanagari": "वस्त्रगोपन",
        "meaning": "Textile Concealment & Pattern Secrecy",
        "houses": [3, 8],
        "planets": ["venus", "ketu"],
        "reason": "Venus fabrics and Ketu secrecy."
    },
    {
        "name": "Dyūta-viśeṣa",
        "devanagari": "द्यूतविशेष",
        "meaning": "Game Theory & Probability Analysis",
        "houses": [5, 11],
        "planets": ["mercury", "rahu"],
        "reason": "5th house speculation and Rahu game theory."
    },
    {
        "name": "Ākarṣa-kṛīḍā",
        "devanagari": "आकर्षक्रीडा",
        "meaning": "Magnetics & Gravitational Physics",
        "houses": [3, 8],
        "planets": ["mars", "saturn"],
        "reason": "Mars magnetic metal force and Saturn gravity."
    },
    {
        "name": "Bālaka-kṛīḍanaka",
        "devanagari": "बालकक्रीडनक",
        "meaning": "Toy Making & Recreational Design",
        "houses": [3, 5],
        "planets": ["mercury", "venus"],
        "reason": "5th house play and Mercury toy engineering."
    },
    {
        "name": "Vainayikī vidyā",
        "devanagari": "वैनायिकी विद्या",
        "meaning": "Pedagogy & Disciplined Mentorship",
        "houses": [5, 9],
        "planets": ["jupiter", "sun"],
        "reason": "9th house Guru and Jupiter moral pedagogy."
    },
    {
        "name": "Vaijayikī vidyā",
        "devanagari": "वैजयिकी विद्या",
        "meaning": "Military Strategy & Competitive Victory",
        "houses": [6, 10],
        "planets": ["mars", "sun"],
        "reason": "6th/10th house competitive victory and Mars warfare."
    },
    {
        "name": "Vaitālikī vidyā",
        "devanagari": "वैतालिकी विद्या",
        "meaning": "Melodic Awakening & Sound Harmonies",
        "houses": [2, 3],
        "planets": ["venus", "moon"],
        "reason": "Venus morning melodies and Moon soothing rhythm."
    }
]


def analyze_kala_vidya(chart_data: dict) -> dict:
    """
    Evaluates and ranks all 64 Classical Kalas from planetary positions and house alignments.
    Returns structured score ranking (/100) and astrological justifications in Devanagari.
    """
    planets = chart_data.get("raw_positions") or chart_data.get("planets") or {}
    houses = chart_data.get("houses") or {}
    yogas = chart_data.get("yogas") or []

    evaluated_kalas = []

    for item in CLASSICAL_64_KALAS:
        score = 62
        reasons = []

        # Evaluate target planets
        for p_name in item["planets"]:
            p_data = planets.get(p_name.lower()) or planets.get(p_name.capitalize()) or {}
            if p_data:
                dig = p_data.get("dignity", "neutral")
                h = p_data.get("house", 0)
                if dig in ["exalted", "own"]:
                    score += 8
                    reasons.append(f"{p_name.capitalize()} {dig}")
                elif dig == "debilitated":
                    score -= 8

                if h in item["houses"]:
                    score += 7
                    reasons.append(f"{p_name.capitalize()} in House {h}")

        # Evaluate house lords
        for h_num in item["houses"]:
            h_info = houses.get(str(h_num), {})
            lord = h_info.get("lord", "").lower()
            if lord in item["planets"]:
                score += 5
                reasons.append(f"Lord of House {h_num} ({lord.capitalize()}) aligned")

        # Evaluate intellectual/creative Yogas
        if yogas:
            score += 5

        final_score = max(40, min(98, score))

        evaluated_kalas.append({
            "name": item["name"],
            "devanagari": item["devanagari"],
            "meaning": item["meaning"],
            "score": final_score,
            "houses": item["houses"],
            "planets": [p.capitalize() for p in item["planets"]],
            "astrological_reason": item["reason"] + (f" ({', '.join(reasons[:2])})" if reasons else "")
        })

    # Sort all 64 Kalas by calculated score
    evaluated_kalas.sort(key=lambda x: x["score"], reverse=True)

    h2 = houses.get("2", {})
    h3 = houses.get("3", {})
    h5 = houses.get("5", {})
    h10 = houses.get("10", {})

    return {
        "top_kalas": evaluated_kalas[:8],
        "all_64_kalas": evaluated_kalas,
        "key_houses": {
            "2nd": f"Sign {h2.get('sign', '?')} (Lord: {h2.get('lord', '?').capitalize()})",
            "3rd": f"Sign {h3.get('sign', '?')} (Lord: {h3.get('lord', '?').capitalize()})",
            "5th": f"Sign {h5.get('sign', '?')} (Lord: {h5.get('lord', '?').capitalize()})",
            "10th": f"Sign {h10.get('sign', '?')} (Lord: {h10.get('lord', '?').capitalize()})",
        }
    }


def format_kala_vidya_subset_context(analysis: dict, profile: dict = None, chart_data: dict = None) -> str:
    """
    Extracts the top 64 classical Kalas AND Student Receptivity pillars in Devanagari for LLM prompting.
    """
    name = profile.get("name", "Seeker") if profile else "Seeker"
    top_k = analysis.get("top_kalas", [])
    kh = analysis.get("key_houses", {})

    kala_lines = [
        f"- {k['devanagari']} / {k['name']} ({k['meaning']}): {k['astrological_reason']}"
        for k in top_k
    ]

    rec_lines = []
    if chart_data:
        rec_analysis = analyze_student_receptivity(chart_data)
        for p in rec_analysis.get("receptivity_pillars", []):
            rec_lines.append(f"- {p['devanagari']} / {p['name']} ({p['meaning']}): {p['indicator']} — {p['status']}")

    rec_block = f"""

[STUDENT COGNITIVE RECEPTIVITY PILLARS IN DEVANAGARI]
{chr(10).join(rec_lines)}""" if rec_lines else ""

    return f"""[64 CLASSICAL VEDIC KALAS & RECEPTIVITY SUBSET: {name.upper()}]
Subject: {name}

[KEY HOUSE LORDS & ALIGNMENTS]
- 2nd House (Speech/Assets): {kh.get('2nd', 'N/A')}
- 3rd House (Skills/Dexterity): {kh.get('3rd', 'N/A')}
- 4th House (Vidya/Foundational Knowledge): Sign {chart_data.get('houses', {}).get('4', {}).get('sign', '?')}
- 5th House (Intellect/Genius): {kh.get('5th', 'N/A')}
- 9th House (Guru Upadesha): Sign {chart_data.get('houses', {}).get('9', {}).get('sign', '?')}
- 10th House (Karma/Action): {kh.get('10th', 'N/A')}

[TOP RANKED CLASSICAL VEDIC KALAS IN DEVANAGARI]
{chr(10).join(kala_lines)}{rec_block}"""



def analyze_student_receptivity(chart_data: dict) -> dict:
    """
    Evaluates student cognitive absorption capacity (Shishya Grahana Shakti), memory retention (Smriti),
    learning style, and receptivity to mastering various Kalas and Vidyas.
    """
    planets = chart_data.get("raw_positions") or chart_data.get("planets") or {}
    houses = chart_data.get("houses") or {}

    h4 = houses.get("4", {})
    h5 = houses.get("5", {})
    h9 = houses.get("9", {})

    merc = planets.get("mercury") or planets.get("Mercury") or {}
    jup = planets.get("jupiter") or planets.get("Jupiter") or {}
    moon = planets.get("moon") or planets.get("Moon") or {}

    # Core Receptivity Pillars (Devanagari)
    pillars = [
        {
            "name": "Smriti Shakti",
            "devanagari": "स्मृति शक्ति",
            "meaning": "Memory Retention & Recall Power",
            "indicator": f"5th House in {h5.get('sign', 'Active')} (Lord: {h5.get('lord', 'Jupiter')})",
            "status": "Strong retention via 5th house intellect"
        },
        {
            "name": "Grahana Capacity",
            "devanagari": "ग्रहण क्षमता",
            "meaning": "Cognitive Absorption Speed",
            "indicator": f"Mercury in {merc.get('sign', 'Air Sign')} (House {merc.get('house', 5)})",
            "status": "Rapid absorption speed powered by Mercury"
        },
        {
            "name": "Ekagrata & Dhayana",
            "devanagari": "एकाग्रता एवं ध्यान",
            "meaning": "Focus & Mental Tranquility",
            "indicator": f"Moon in {moon.get('sign', 'Exalted')} (House {moon.get('house', 4)})",
            "status": "Calm focus supported by Moon placement"
        },
        {
            "name": "Guru Receptivity",
            "devanagari": "गुरु उपदेश ग्रहण",
            "meaning": "Receptivity to Mentors & Sacred Vidyas",
            "indicator": f"9th House in {h9.get('sign', 'Dharma')} with Jupiter alignment",
            "status": "High receptivity to Guru guidance & ethical wisdom"
        }
    ]

    return {
        "receptivity_pillars": pillars,
        "primary_learning_style": "Visual & Analytical (Drishya-Tarka)",
        "key_houses": {
            "4th_vidya": f"Sign {h4.get('sign', '?')} (Lord: {h4.get('lord', '?')})",
            "5th_buddhi": f"Sign {h5.get('sign', '?')} (Lord: {h5.get('lord', '?')})",
            "9th_guru": f"Sign {h9.get('sign', '?')} (Lord: {h9.get('lord', '?')})",
        }
    }


def format_student_receptivity_subset_context(analysis: dict, profile: dict = None) -> str:
    """
    Formats the student receptivity astrological subset context for LLM prompting.
    """
    name = profile.get("name", "Student") if profile else "Student"
    pillars = analysis.get("receptivity_pillars", [])
    kh = analysis.get("key_houses", {})

    pillar_lines = [
        f"- {p['devanagari']} / {p['name']} ({p['meaning']}): {p['indicator']} — {p['status']}"
        for p in pillars
    ]

    return f"""[STUDENT RECEPTIVITY ASTROLOGICAL SUBSET: {name.upper()}]
Student Name: {name}

[EDUCATIONAL & RECEPTIVITY HOUSES]
- 4th House (Vidya/Foundational Knowledge): {kh.get('4th_vidya', 'N/A')}
- 5th House (Buddhi/Memory Retention): {kh.get('5th_buddhi', 'N/A')}
- 9th House (Guru Upadesha/Higher Vidyas): {kh.get('9th_guru', 'N/A')}

[COGNITIVE RECEPTIVITY PILLARS IN DEVANAGARI]
{chr(10).join(pillar_lines)}"""

