import { useState, useRef } from 'react'
import { formatSignWithHindi } from '../../utils/hindiMapping'

interface KalaVidyaDashboardProps {
  chartData: any
}

interface ClassicalKalaRule {
  name: string
  devanagari: string
  meaning: string
  houses: number[]
  planets: string[]
  examples: string
  masteryMethod: string
}

const ALL_64_KALAS_RULES: ClassicalKalaRule[] = [
  { name: 'Gīta vidyā', devanagari: 'गीतविद्या', meaning: 'Vocal Music & Singing', houses: [2, 3, 5], planets: ['venus', 'mercury', 'moon'], examples: 'Classical vocal performance, opera, acoustic sound design, voice modulation coaching, podcasting.', masteryMethod: 'Practice daily svara scales, breath control (pranayama), ear tuning, and vocal pitch exercise.' },
  { name: 'Vādya vidyā', devanagari: 'वाद्यविद्या', meaning: 'Instrumental Music', houses: [3, 5], planets: ['venus', 'mercury', 'mars'], examples: 'Playing string/percussion instruments, synthesizer programming, sound engineering, orchestration.', masteryMethod: 'Daily finger dexterity drills, rhythmic tempo practice (Tala), and multi-instrumental ensemble playing.' },
  { name: 'Nṛtya vidyā', devanagari: 'नृत्यविद्या', meaning: 'Dance & Movement', houses: [3, 5, 1], planets: ['venus', 'mars'], examples: 'Choreography, classical dance (Bharatanatyam/Kathak), somatic movement therapy, stage performance.', masteryMethod: 'Mastering posture (Mudra), rhythmic footwork, flexibility conditioning, and expressive storytelling.' },
  { name: 'Nāṭya vidyā', devanagari: 'नाट्यविद्या', meaning: 'Theatrical Acting & Drama', houses: [3, 5, 10], planets: ['venus', 'rahu', 'mercury'], examples: 'Stage acting, film directing, character voice acting, public drama productions, screenwriting.', masteryMethod: 'Improv workshops, emotional resonance exercises, script memorization, and body language mastery.' },
  { name: 'Ālekhya vidyā', devanagari: 'आलेख्यविद्या', meaning: 'Painting & Fine Arts', houses: [3, 4, 5], planets: ['venus', 'moon'], examples: 'Oil painting, digital illustration, UI/UX graphic design, visual storyboarding, concept art.', masteryMethod: 'Color theory study, perspective drafting, daily sketching from life, and mastering digital/physical media.' },
  { name: 'Viśeṣaka-cchēdya vidyā', devanagari: 'विशेषकच्छेद्यविद्या', meaning: 'Body Decoration & Cosmetology', houses: [1, 3], planets: ['venus', 'mercury'], examples: 'Makeup artistry, cosmetic tattooing, body painting, prosthetic effects design, personal grooming.', masteryMethod: 'Facial anatomy study, color blending techniques, skin-safe product formulation, and precision brushwork.' },
  { name: 'Tāṇḍula-kusuma-balivikāra', devanagari: 'ताण्डुलकुसुमबलिविकार', meaning: 'Preparing Sacred Offerings', houses: [5, 9], planets: ['jupiter', 'sun'], examples: 'Ritual design, sacred geometry altars, ceremonial event management, mandalas.', masteryMethod: 'Study of sacred geometry, Vedic ritual mantras, ritualistic flower/grain arrangements, and mindfulness.' },
  { name: 'Puṣpastaraṇa', devanagari: 'पुष्पास्तरण', meaning: 'Floral Bed & Spatial Design', houses: [4, 12], planets: ['venus', 'moon'], examples: 'Landscape architecture, luxury interior spatial design, floral installations, spa aesthetics.', masteryMethod: 'Botanic arrangement, spatial harmony (Vastu), sensory lighting design, and natural texture pairing.' },
  { name: 'Danta-vasanāṅga-rāga', devanagari: 'दन्तवसनाङ्गराग', meaning: 'Perfumes & Hygiene Products', houses: [2, 6], planets: ['venus', 'mercury'], examples: 'Organic cosmetics creation, natural skincare formulation, dental hygiene product crafting, aromatherapy.', masteryMethod: 'Essential oil chemistry, herb extraction techniques, dermatological safety testing, and scent profiling.' },
  { name: 'Maṇi-bhūmikā-karma', devanagari: 'मणिभूमिकाकर्म', meaning: 'Jewel Settings & Gemology', houses: [2, 3, 11], planets: ['sun', 'venus', 'mars'], examples: 'Jewelry manufacturing, gemstone appraisal, mosaic tile setting, luxury watchmaking.', masteryMethod: 'Micro-welding skills, gem refraction testing, CAD jewelry modeling, and precious metal alloy casting.' },
  { name: 'Śayyā-racana', devanagari: 'शय्यारचन', meaning: 'Arranging Bedding & Comfort', houses: [4, 12], planets: ['venus', 'moon'], examples: 'Luxury hotel hospitality management, ergonomic mattress engineering, interior relaxation design.', masteryMethod: 'Ergonomic sleep science, high-thread textile selection, spatial acoustics, and ambient lighting.' },
  { name: 'Udaka-vādya', devanagari: 'उदकवाद्य', meaning: 'Acoustic Music with Water', houses: [3, 4], planets: ['moon', 'venus'], examples: 'Hydro-acoustic instruments, water fountain musical choreography, underwater audio engineering.', masteryMethod: 'Fluid dynamics acoustics, aquatic pitch tuning, and glass/water resonance calibration.' },
  { name: 'Udaka-ghāta', devanagari: 'उदकघात', meaning: 'Water Hydraulics & Splashing Sports', houses: [4, 5], planets: ['moon', 'mars'], examples: 'Water park engineering, competitive swimming coaching, hydraulic pump mechanics, jet ski sport.', masteryMethod: 'Hydrodynamics engineering, aquatic propulsion techniques, and water pressure control.' },
  { name: 'Citra-yoga', devanagari: 'चित्रयोग', meaning: 'Pigment & Color Formulation', houses: [3, 5], planets: ['mercury', 'venus'], examples: 'Industrial dye synthesis, digital color grading, paint chemistry, printing ink formulation.', masteryMethod: 'Chemical pigment mixing, spectrography, lighting environment calibration, and digital color profiles.' },
  { name: 'Mālya-grathana-vikalpa', devanagari: 'माल्यग्रथनविकल्प', meaning: 'Floral Garland Synthesis', houses: [3, 5], planets: ['venus', 'mercury'], examples: 'Botanical design, high-end wedding floral weaving, artificial flower crafting, horticulture styling.', masteryMethod: 'Botanical preservation, wire-frame floral weaving, and color symmetry coordination.' },
  { name: 'Śekharāpīḍa-yojana', devanagari: 'शेखरापीडयोजन', meaning: 'Coronet & Crown Crafting', houses: [1, 10], planets: ['sun', 'venus'], examples: 'Royal headgear craftsmanship, luxury hat/millinery design, theatrical crown props.', masteryMethod: 'Metal wire shaping, velvet/gem setting on headpieces, and ergonomic headwear balance.' },
  { name: 'Nēpathyayoga', devanagari: 'नेपथ्ययोग', meaning: 'Costume & Fashion Design', houses: [3, 10], planets: ['venus', 'rahu'], examples: 'Fashion haute couture, theatrical wardrobe design, celebrity styling, textile pattern making.', masteryMethod: 'Garment draping, pattern drafting, fabric durability testing, and runway trend forecasting.' },
  { name: 'Karṇapātra-bhaṅga', devanagari: 'कर्णपत्रभङ्ग', meaning: 'Ear Ornament Carving', houses: [3, 2], planets: ['venus', 'mercury'], examples: 'Fine ear jewelry carving, filigree ear cuff design, acoustic earpiece custom molding.', masteryMethod: 'Micro-carving precision, precious metal soldering, and ear cartilage ergonomics.' },
  { name: 'Sugandha-yukti', devanagari: 'सुगन्धयुक्ति', meaning: 'Perfumery & Fragrance Synthesis', houses: [2, 5], planets: ['venus', 'jupiter'], examples: 'Master perfumer (Nose), luxury fragrance creation, candle scenting, aroma marketing.', masteryMethod: 'Olfactory notes profiling (top, heart, base notes), natural maceration, and aroma chemistry.' },
  { name: 'Bhūṣaṇa-yojana', devanagari: 'भूषणयोजन', meaning: 'Ornamentation & Jewelry Styling', houses: [2, 1], planets: ['venus', 'sun'], examples: 'Luxury fashion styling, personal image consulting, bridal jewelry curation, high-end accessories.', masteryMethod: 'Wardrobe silhouette matching, metal-tone skin analysis, and luxury accessory pairing.' },
  { name: 'Aindra-jāla', devanagari: 'ऐन्द्रजाल', meaning: 'Illusion, Magic & Sleight of Hand', houses: [3, 5, 8], planets: ['rahu', 'mercury'], examples: 'Stage magic, illusion design, CGI visual effects, mentalism performance, escape art.', masteryMethod: 'Misdirection psychology, sleight of hand mechanics, optical illusion physics, and stagecraft.' },
  { name: 'Kaucumāra', devanagari: 'कौचुमार', meaning: 'Esoteric & Mystic Arts', houses: [8, 12], planets: ['ketu', 'jupiter'], examples: 'Occult studies, tantric Kundalini practices, herbal elixir creation, energetic healing.', masteryMethod: 'Mantra sadhana, pranayama energy channel clearing, and ancient manuscript decoding.' },
  { name: 'Hasta-lāghava', devanagari: 'हस्तलाघव', meaning: 'Manual Precision & Fine Mechanics', houses: [3], planets: ['mercury', 'mars'], examples: 'Surgical dexterity, micro-assembly, typing speed, arcade/gaming reflexes, watch repair.', masteryMethod: 'Finger dexterity exercises, hand-eye coordination training, and micro-tool handling.' },
  { name: 'Citra-śākā-pūpa-bhakṣya-vikāra-kriyā', devanagari: 'चित्रशाकापूपभक्ष्यविकारक्रिया', meaning: 'Gourmet Culinary Arts', houses: [2, 4], planets: ['moon', 'venus', 'mars'], examples: 'Executive chef, pastry arts, molecular gastronomy, food styling & plating, restaurant management.', masteryMethod: 'Flavor pairing chemistry, knife technique, temperature-controlled cooking, and plating art.' },
  { name: 'Pānaka-rasa-rāgāsava-yojana', devanagari: 'पानकरसरागासवयोजन', meaning: 'Mixology & Beverage Crafting', houses: [2, 5], planets: ['moon', 'venus'], examples: 'Craft mixology, sommelier wine tasting, botanical beverage brewing, artisan tea formulation.', masteryMethod: 'Fermentation science, flavor balancing (sweet, sour, bitter), and liquid infusion methods.' },
  { name: 'Sūci-vāya-karma', devanagari: 'सूचिवायकर्म', meaning: 'Needlework, Embroidery & Weaving', houses: [3], planets: ['venus', 'mercury'], examples: 'Textile weaving, haute couture hand embroidery, tapestry design, leather stitching.', masteryMethod: 'Stitch technique precision, loom weaving mechanics, and thread tension control.' },
  { name: 'Sūtra-kṛīḍā', devanagari: 'सूत्रक्रीडा', meaning: 'Puppetry & String Mechanics', houses: [3, 5], planets: ['mercury', 'rahu'], examples: 'Marionette puppetry, animatronics control, stop-motion animation, string puppet theater.', masteryMethod: 'Pulley and string tension mechanics, character voice acting, and synchronized movement.' },
  { name: 'Vīṇā-ḍamaruka-vādya', devanagari: 'वीणाडमरुकवाद्य', meaning: 'String Instrument & Percussion', houses: [3, 5], planets: ['venus', 'mars'], examples: 'Sitar/Veena performance, drumming, acoustic resonance testing, music composition.', masteryMethod: 'Rhythmic speed drills, string tension tuning, and acoustic chamber resonance study.' },
  { name: 'Prahelikā', devanagari: 'प्रहेलिका', meaning: 'Riddles & Logic Puzzles', houses: [5], planets: ['mercury', 'ketu'], examples: 'Puzzle design, escape room creation, riddle writing, logic board game engineering.', masteryMethod: 'Mathematical logic trees, lateral thinking exercises, and player psychology testing.' },
  { name: 'Durvacaka-yoga', devanagari: 'दुर्वचकयोग', meaning: 'Cryptography & Conundrums', houses: [2, 5], planets: ['mercury', 'rahu'], examples: 'Cybersecurity, blockchain encryption, cryptographic hashing, codebreaking, data security.', masteryMethod: 'Algorithm analysis, modular arithmetic, prime factorization, and penetration testing.' },
  { name: 'Pustaka-vācana', devanagari: 'पुस्तकवाचन', meaning: 'Literary Recitation & Reading', houses: [2, 4, 5], planets: ['mercury', 'jupiter'], examples: 'Audiobook narration, literary critique, public reading, voiceover artist, academic lecturing.', masteryMethod: 'Diction and articulation practice, tone pacing, storytelling cadence, and speed reading.' },
  { name: 'Nāṭikā-khyāyikā-darśana', devanagari: 'नाटिकाख्यायिकादर्शन', meaning: 'Storytelling & Enactment', houses: [3, 5], planets: ['mercury', 'moon'], examples: 'Screenwriting, novel writing, narrative game design, mythic folklore retelling.', masteryMethod: 'Story arc structuring, character development, dialogue pacing, and audience emotional resonance.' },
  { name: 'Kāvya-samasya-pūraṇa', devanagari: 'काव्यसमस्यापूरण', meaning: 'Poetic Verse Composition', houses: [2, 5], planets: ['venus', 'jupiter', 'mercury'], examples: 'Poetry composition, lyric writing for songs, rhyming verse creation, literary copywriting.', masteryMethod: 'Meter and prosody study (Chanda), vocabulary expansion, and metaphorical expression.' },
  { name: 'Paṭṭikā-vetra-bāṇa-vikalpa', devanagari: 'पट्टिकावेत्रबाणविकल्प', meaning: 'Weapons, Armor & Shield Crafting', houses: [3, 6], planets: ['mars', 'saturn'], examples: 'Defense equipment engineering, archery equipment design, protective gear, martial arts weaponry.', masteryMethod: 'Tensile strength metallurgy, ballistic testing, ergonomic grip design, and safety forging.' },
  { name: 'Tarku-karma', devanagari: 'तर्कुकर्म', meaning: 'Spindle Spinning & Fiber Tech', houses: [3], planets: ['saturn', 'mercury'], examples: 'Synthetic fiber engineering, yarn spinning technology, eco-textile manufacturing.', masteryMethod: 'Fiber elasticity testing, automated spinning wheel maintenance, and eco-dyeing.' },
  { name: 'Takṣaṇa', devanagari: 'तक्षण', meaning: 'Carpentry & Structural Woodwork', houses: [4, 3], planets: ['mars', 'saturn'], examples: 'Custom furniture design, wooden architecture, timber joinery, CNC router woodworking.', masteryMethod: 'Wood grain identification, precision chisel/saw handling, joinery engineering, and wood finishing.' },
  { name: 'Vāstu-vidyā', devanagari: 'वास्तुविद्या', meaning: 'Architecture & Engineering', houses: [4, 10], planets: ['mars', 'saturn', 'venus'], examples: 'Building architecture, structural civil engineering, Vastu Shastra spatial design, BIM modeling.', masteryMethod: 'CAD drafting, structural load calculation, environmental solar orientation, and spatial geometry.' },
  { name: 'Raupya-ratna-parīkṣā', devanagari: 'रौप्यरत्नपरीक्षा', meaning: 'Testing Gems & Metals', houses: [2, 5, 11], planets: ['sun', 'mercury', 'jupiter'], examples: 'Gemological laboratory testing, gold/silver purity assaying, mineral trade inspection.', masteryMethod: 'Refractometer gem analysis, specific gravity testing, spectrographic assaying, and grading.' },
  { name: 'Dhātu-vāda', devanagari: 'धातुवाद', meaning: 'Metallurgy & Materials Science', houses: [3, 10], planets: ['mars', 'saturn'], examples: 'Metallurgical engineering, alloy creation, aerospace materials science, 3D metal printing.', masteryMethod: 'Heat treatment processes, crystal lattice stress analysis, and alloy composition testing.' },
  { name: 'Maṇi-rāga-jñāna', devanagari: 'मणिशरागज्ञान', meaning: 'Jewel Dyeing & Coloration', houses: [2, 5], planets: ['venus', 'sun'], examples: 'Gemstone color enhancement, synthetic gem creation, optical glass tinting.', masteryMethod: 'Thermal gem enhancement, chemical diffusion coloration, and light refraction testing.' },
  { name: 'Ākāra-jñāna', devanagari: 'आकारज्ञान', meaning: 'Mineralogy & Geology', houses: [4, 8], planets: ['saturn', 'mars'], examples: 'Geological surveying, mining engineering, petroleum exploration, soil science.', masteryMethod: 'Core sample analysis, seismic geological mapping, mineral crystal identification, and field survey.' },
  { name: 'Vṛkṣāyurveda-yoga', devanagari: 'वृक्षायुर्वेदयोग', meaning: 'Botany & Herbal Healing', houses: [4, 6], planets: ['mercury', 'jupiter', 'sun'], examples: 'Ayurvedic herbalism, botanical pharmacology, organic farming, plant pathology.', masteryMethod: 'Plant taxonomy, herbal extraction protocols, soil organic chemistry, and cultivation.' },
  { name: 'Meṣa-kukkuṭa-lāvaka-yuddha-vidhi', devanagari: 'मेषकुक्कुटलावकयुद्धविधि', meaning: 'Animal Behavior & Training', houses: [6], planets: ['mars', 'saturn'], examples: 'Veterinary science, K9 police dog training, equestrian dressage, wildlife rehabilitation.', masteryMethod: 'Animal ethology study, positive reinforcement conditioning, and animal health management.' },
  { name: 'Śuka-sārikā-pralāpana', devanagari: 'शुकसारिकाप्रलापन', meaning: 'Avian Speech Training', houses: [2, 3], planets: ['mercury', 'jupiter'], examples: 'Ornithology, parrot speech training, avian bioacoustics research, zoo bird care.', masteryMethod: 'Audio mimicry conditioning, avian dietary optimization, and vocal repetition schedule.' },
  { name: 'Utsādana', devanagari: 'उत्सादन', meaning: 'Massage Therapy & Hygiene', houses: [1, 6], planets: ['mars', 'venus'], examples: 'Ayurvedic Abhyanga massage, physiotherapy, sports recovery therapy, spa bodywork.', masteryMethod: 'Musculoskeletal anatomy, pressure point (Marma) therapy, and therapeutic oil warming.' },
  { name: 'Keśa-mārjana-kauśala', devanagari: 'केशमार्जनकौशल', meaning: 'Trichology & Hair Styling', houses: [1, 3], planets: ['venus', 'mercury'], examples: 'Trichology clinic consulting, celebrity hairstyling, scalp treatment formulation.', masteryMethod: 'Scalp microscopic analysis, hair kerating chemistry, precision scissor cutting, and styling.' },
  { name: 'Akṣara-muṣṭika-kathana', devanagari: 'अक्षरमुष्टिकाकथन', meaning: 'Sign Language & Gestures', houses: [3], planets: ['mercury'], examples: 'Sign language interpretation (ASL/ISL), non-verbal gesture communication, body language analysis.', masteryMethod: 'Finger spelling fluency, facial expression coordination, and kinetic gesture speed.' },
  { name: 'Dhāraṇa-mātrikā', devanagari: 'धारणामात्रिका', meaning: 'Protective Amulets & Yantras', houses: [5, 9], planets: ['jupiter', 'ketu'], examples: 'Talisman consecration, Yantra engraving, protective energy field work, sacred geometry.', masteryMethod: 'Yantra copper plate etching, ritual mantra consecration, and planetary gem alignment.' },
  { name: 'Deśa-bhāṣā-jñāna', devanagari: 'देशभाषाज्ञान', meaning: 'Linguistics & Regional Dialects', houses: [2, 3, 9], planets: ['mercury', 'jupiter'], examples: 'Polyglot translation, computational linguistics, language localization, dialect coaching.', masteryMethod: 'Phonetic alphabet mastery, grammar syntax dissection, immersion practice, and translation.' },
  { name: 'Nirmiti-jñāna', devanagari: 'निर्मितिज्ञान', meaning: 'Predictive Science & Omens', houses: [5, 8, 9], planets: ['jupiter', 'ketu'], examples: 'Astrological counseling, predictive data analytics, trend forecasting, intuitive synthesis.', masteryMethod: 'Jyotish chart calculation, Dasha timing analysis, omen (Nimitta) observation, and synthesis.' },
  { name: 'Yantra-mātrikā', devanagari: 'यन्त्रमात्रिका', meaning: 'Mechanics, Robotics & Systems', houses: [3, 5, 10], planets: ['saturn', 'mars', 'mercury', 'rahu'], examples: 'Industrial robotics, mechanical CAD design, automated machinery, embedded IoT systems.', masteryMethod: 'Kinematic link calculation, CAD modeling, micro-controller programming, and motor gear assembly.' },
  { name: 'Mlecchita-kutarka-vikalpa', devanagari: 'म्लेच्छितकुतर्कविकल्प', meaning: 'Foreign Logic & Debating', houses: [3, 6, 9], planets: ['mercury', 'rahu'], examples: 'International diplomacy, cross-cultural legal debate, geopolitical analysis, negotiation.', masteryMethod: 'Comparative legal study, rhetorical counter-arguments, logic fallacies identification, and debate.' },
  { name: 'Saṁvācya', devanagari: 'संवाच्य', meaning: 'Oratory, Speech & Dialogue', houses: [2, 3, 10], planets: ['mercury', 'jupiter'], examples: 'Keynote public speaking, debate, podcast hosting, political campaigning, corporate PR.', masteryMethod: 'Vocal projection drills, rhetorical structure crafting, audience engagement, and stance control.' },
  { name: 'Mānasi kāvya-kriyā', devanagari: 'मानसी काव्यक्रिया', meaning: 'Mental Poetic Composition', houses: [5], planets: ['venus', 'moon', 'jupiter'], examples: 'Instantaneous poetic improvisation, rap freestyle lyricism, mental creative visualization.', masteryMethod: 'Rhyme scheme speed drills, mental imagery holding, and flow-state creative exercises.' },
  { name: 'Kriyā-vikalpa', devanagari: 'क्रियाविकल्प', meaning: 'Therapeutic Design & Remedies', houses: [5, 6, 9], planets: ['jupiter', 'sun'], examples: 'Holistic wellness consulting, astrological remediation, lifestyle prescription, habit design.', masteryMethod: 'Vedic remedy formulation (Mantra/Yantra/Gem), habit tracking design, and lifestyle audit.' },
  { name: 'Calitaka-yoga', devanagari: 'चलितकयोग', meaning: 'Sacred Shrine Architecture', houses: [4, 9], planets: ['jupiter', 'saturn'], examples: 'Sacred temple architecture, sanctuary design, meditation space planning, heritage restoration.', masteryMethod: 'Sacred geometry proportioning, stone carving alignment, and directional acoustics.' },
  { name: 'Abhidhāna-kośa-chanda-jñāna', devanagari: 'अभिधानकोशछन्दोज्ञान', meaning: 'Lexicography & Prosody', houses: [2, 5], planets: ['mercury', 'jupiter'], examples: 'Dictionary editing, poetic meter analysis, NLP text corpus curation, etymology research.', masteryMethod: 'Sanskrit root (Dhatu) analysis, poetic meter breakdown, and dictionary indexing.' },
  { name: 'Vastra-gopana', devanagari: 'वस्त्रगोपन', meaning: 'Textile Concealment Art', houses: [3, 8], planets: ['venus', 'ketu'], examples: 'High-security garment pockets, tactical military apparel design, hidden lining tailoring.', masteryMethod: 'Concealed stitch techniques, waterproof lining integration, and covert pocket design.' },
  { name: 'Dyūta-viśeṣa', devanagari: 'द्यूतविशेष', meaning: 'Game Theory & Probability', houses: [5, 11], planets: ['mercury', 'rahu'], examples: 'Algorithmic trading, game theory strategy, poker analytics, mathematical odds modeling.', masteryMethod: 'Probability distribution calculation, risk-reward ratio modeling, and game strategy simulation.' },
  { name: 'Ākarṣa-kṛīḍā', devanagari: 'आकर्षक्रीडा', meaning: 'Magnetics & Physics Play', houses: [3, 8], planets: ['mars', 'saturn'], examples: 'Electromagnetic hardware design, magnetic levitation engineering, physics lab demonstration.', masteryMethod: 'Electromagnetism calculations, coil winding, magnetic field mapping, and physics experiments.' },
  { name: 'Bālaka-kṛīḍanaka', devanagari: 'बालकक्रीडनक', meaning: 'Toy Crafting & Recreation', houses: [3, 5], planets: ['mercury', 'venus'], examples: 'Educational toy design, children board game creation, STEM learning kit development.', masteryMethod: 'Child safety materials testing, playful UX design, and interactive mechanical assembly.' },
  { name: 'Vainayikī vidyā', devanagari: 'वैनायिकी विद्या', meaning: 'Pedagogy & Discipline', houses: [5, 9], planets: ['jupiter', 'sun'], examples: 'School principal leadership, educational curriculum design, student coaching, ethics teaching.', masteryMethod: 'Pedagogical framework design, student behavioral coaching, and ethical policy drafting.' },
  { name: 'Vaijayikī vidyā', devanagari: 'वैजयिकी विद्या', meaning: 'Military Strategy & Victory', houses: [6, 10], planets: ['mars', 'sun'], examples: 'Corporate business strategy, competitive athletics coaching, tactical crisis leadership.', masteryMethod: 'Competitive SWOT analysis, tactical positioning, morale building, and execution speed.' },
  { name: 'Vaitālikī vidyā', devanagari: 'वैतालिकी विद्या', meaning: 'Melodic Awakening Music', houses: [2, 3], planets: ['venus', 'moon'], examples: 'Sound bath therapy, morning raga vocal performance, circadian music composition.', masteryMethod: 'Morning Raga pitch tuning, singing bowl acoustics, and circadian rhythm sound alignment.' },
]

export default function KalaVidyaDashboard({ chartData }: KalaVidyaDashboardProps) {
  const explorerRef = useRef<HTMLDivElement>(null)

  const houses = chartData?.houses || {}
  const rawPositions = chartData?.raw_positions || chartData?.planets || {}
  const yogas = chartData?.yogas || []

  const h3 = houses['3'] || {}
  const h4 = houses['4'] || {}
  const h5 = houses['5'] || {}
  const h9 = houses['9'] || {}

  const [selectedKalaName, setSelectedKalaName] = useState<string>(ALL_64_KALAS_RULES[50].name)

  // Dynamic Kala evaluation algorithm
  const evaluatedKalas = ALL_64_KALAS_RULES.map((item) => {
    let score = 62
    let reasons: string[] = []

    for (const pName of item.planets) {
      const pData =
        rawPositions[pName] ||
        rawPositions[pName.toLowerCase()] ||
        rawPositions[pName.charAt(0).toUpperCase() + pName.slice(1)]
      if (pData) {
        const dig = (pData.dignity || 'neutral').toLowerCase()
        const h = pData.house || 0
        if (dig === 'exalted' || dig === 'own') {
          score += 8
          reasons.push(`${pName.toUpperCase()} is ${dig} in house ${h}`)
        } else if (dig === 'debilitated') {
          score -= 8
        }
        if (item.houses.includes(h)) {
          score += 7
          reasons.push(`${pName.toUpperCase()} occupies house ${h}`)
        }
      }
    }
    for (const hNum of item.houses) {
      const hInfo = houses[String(hNum)]
      if (hInfo && hInfo.lord && item.planets.includes(hInfo.lord.toLowerCase())) {
        score += 5
        reasons.push(`House ${hNum} lord ${hInfo.lord.toUpperCase()} aligns with key planet`)
      }
    }
    if (yogas.length > 0) score += 5

    const isTopAligned = score >= 72

    return {
      ...item,
      score: Math.max(40, Math.min(98, score)),
      isTopAligned,
      reasonSummary: isTopAligned
        ? `✨ Highly Aligned: ${reasons.length > 0 ? reasons.join('; ') : 'Primary house lords and planetary dignities directly energize this Kala.'}`
        : `⚖️ Secondary Alignment: Planetary lords are neutral in your birth chart, meaning this Vidya can be developed through focused practice and study.`
    }
  })

  evaluatedKalas.sort((a, b) => b.score - a.score)
  const top6Kalas = evaluatedKalas.slice(0, 6)

  const selectedKalaEval = evaluatedKalas.find((k) => k.name === selectedKalaName) || evaluatedKalas[0]

  const handleSelectKala = (name: string) => {
    setSelectedKalaName(name)
    setTimeout(() => {
      explorerRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }, 50)
  }



  // Enriched Receptivity Pillars with Deep Horoscope Analysis
  const receptivityPillars = [
    {
      devanagari: 'Smriti Shakti',
      name: 'Smriti Shakti',
      title: 'Memory Retention & Recall Power',
      astrologicalDriver: `Governed by 5th House in ${h5.sign ? formatSignWithHindi(h5.sign) : 'Active'} (Lord: ${h5.lord || 'Jupiter'}) & Jupiter alignment.`,
      desc: 'How long-term memory operates, recall speed under exam/work stress, and retention of complex Vidyas.',
      icon: 'psychology',
      deepAnalysis: `Your 5th House (Buddhi, Smriti & Intellect) is placed in ${h5.sign ? formatSignWithHindi(h5.sign) : 'an active sign'}. This alignment gives your brain structured memory storage capacity. You retain information best when concepts are organized logically rather than crammed passively.`,
      cognitiveCharacteristics: [
        'High long-term retention for structured data and core principles',
        'Recall speed is enhanced when concepts are connected to practical visual frameworks',
        'Memory fatigue occurs during unstructured passive reading — active recall is key'
      ],
      studyMethod: 'Abhyasa-Smriti (Spaced active recall with interval self-testing and mnemonic visualization).'
    },
    {
      devanagari: 'Grahana Capacity',
      name: 'Grahana Capacity',
      title: 'Cognitive Absorption Speed',
      astrologicalDriver: `Powered by Mercury logic processing, 3rd House skills, and 4th House Vidya in ${h4.sign ? formatSignWithHindi(h4.sign) : 'Active'}.`,
      desc: 'Speed of processing new complex concepts, abstract logic absorption, and multidisciplinary synthesis.',
      icon: 'bolt',
      deepAnalysis: `Your 4th House (Foundational Learning & Vidya) and Mercury placement govern your cognitive absorption speed. You absorb complex logic rapidly when presented with first-principles or real-world architectural flows.`,
      cognitiveCharacteristics: [
        'Rapid initial concept absorption — grasps core logic faster than peers',
        'Thrives on first-principles analysis and structural breakdown',
        'May experience boredom if learning pace is slow or overly repetitive'
      ],
      studyMethod: 'Drishya-Tarka (Socratic active inquiry combined with interactive concept mapping).'
    },
    {
      devanagari: 'Ekagrata & Dhyana',
      name: 'Ekagrata & Dhyana',
      title: 'Focus & Mental Tranquility',
      astrologicalDriver: `Supported by Moon emotional stability and 4th House mental composure (${h4.sign ? formatSignWithHindi(h4.sign) : 'Tranquil'}).`,
      desc: 'Concentration duration, immunity to digital distractions, and mental stamina during deep work.',
      icon: 'self_improvement',
      deepAnalysis: `Your mental focus (Ekagrata) is anchored by your Moon sign and 4th house tranquility. When your study environment is peaceful and uncluttered, your mind enters a deep flow state (Dhyana) effortlessly.`,
      cognitiveCharacteristics: [
        'Deep focus flow state achievable for 90+ minute uninterrupted blocks',
        'Susceptible to cognitive fragmentation if study environment is noisy or chaotic',
        'Mental stamina peaks when learning sessions begin with brief breath mindfulness'
      ],
      studyMethod: 'Pranayama-Dhyana (5-minute breath grounding before study sessions & 50/10 Pomodoro flow).'
    },
    {
      devanagari: 'Guru Receptivity',
      name: 'Guru Receptivity',
      title: 'Mentor Wisdom & Sacred Vidya Assimilation',
      astrologicalDriver: `Governed by 9th House in ${h9.sign ? formatSignWithHindi(h9.sign) : 'Dharma'} (Lord: ${h9.lord || 'Jupiter'}) for higher learning.`,
      desc: 'Receptivity to mentors, teachers, ethical guidance, and sacred lineage wisdom.',
      icon: 'diversity_3',
      deepAnalysis: `Your 9th House governs higher wisdom (Guru Upadesha) and ethical learning. You absorb wisdom exponentially faster when guided by a respected mentor or expert teacher who leads by authentic example.`,
      cognitiveCharacteristics: [
        'High receptivity to direct 1-on-1 mentorship and masterclass instruction',
        'Deep respect for ethical principles and lineage wisdom in your chosen field',
        'Accelerated growth when participating in master-apprentice (Guru-Shishya) dynamics'
      ],
      studyMethod: 'Guru-Vada (Direct Q&A dialogic sessions with experienced mentors and peer teaching).'
    }
  ]

  const getReceptivityPower = (pillarName: string) => {
    let score = 75
    const h5Lord = (h5.lord || '').toLowerCase()
    const h9Lord = (h9.lord || '').toLowerCase()
    const p5Data = rawPositions[h5Lord]
    const p9Data = rawPositions[h9Lord]
    const mercData = rawPositions['mercury']
    const moonData = rawPositions['moon']
    const jupData = rawPositions['jupiter']

    if (pillarName === 'Smriti Shakti') {
      if (p5Data) {
        const dig = (p5Data.dignity || '').toLowerCase()
        if (dig === 'exalted' || dig === 'own') score += 15
        else if (dig === 'debilitated') score -= 15
      }
    } else if (pillarName === 'Grahana Capacity') {
      if (mercData) {
        const dig = (mercData.dignity || '').toLowerCase()
        if (dig === 'exalted' || dig === 'own') score += 15
        else if (dig === 'debilitated') score -= 15
      }
    } else if (pillarName === 'Ekagrata & Dhyana') {
      if (moonData) {
        const dig = (moonData.dignity || '').toLowerCase()
        if (dig === 'exalted' || dig === 'own') score += 15
        else if (dig === 'debilitated') score -= 15
      }
    } else if (pillarName === 'Guru Receptivity') {
      if (p9Data) {
        const dig = (p9Data.dignity || '').toLowerCase()
        if (dig === 'exalted' || dig === 'own') score += 8
      }
      if (jupData) {
        const dig = (jupData.dignity || '').toLowerCase()
        if (dig === 'exalted' || dig === 'own') score += 8
        else if (dig === 'debilitated') score -= 10
      }
    }
    const finalScore = Math.min(98, Math.max(50, score))
    let level = 'Moderate'
    if (finalScore >= 88) level = 'Outstanding'
    else if (finalScore >= 78) level = 'Strong'
    else if (finalScore >= 65) level = 'Moderate'
    else level = 'Average'
    return { score: finalScore, level }
  }



  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Top Banner & Quick Metrics */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-600">
              <span className="material-symbols-outlined text-2xl">school</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-display text-2xl font-bold text-primary">
                  64 Kalas & Student Receptivity (६४ कलाएँ एवं शिष्य ग्रहण क्षमता)
                </h3>
                <span className="text-[11px] font-extrabold bg-primary-fixed text-primary px-2.5 py-0.5 rounded-full">
                  Unified Vedic Engine
                </span>
              </div>
              <p className="text-xs text-on-surface-variant font-medium mt-0.5">
                64 Classical Kalas, Cognitive Absorption (Grahana Shakti) & Interactive Kala Explorer
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs">
              <span className="text-on-surface-variant block text-[10px] font-semibold">3rd (Skills)</span>
              <strong className="text-primary font-bold">{h3.sign ? formatSignWithHindi(h3.sign) : 'Active'}</strong>
            </div>
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs">
              <span className="text-on-surface-variant block text-[10px] font-semibold">4th (Vidya)</span>
              <strong className="text-primary font-bold">{h4.sign ? formatSignWithHindi(h4.sign) : 'Active'}</strong>
            </div>
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs">
              <span className="text-on-surface-variant block text-[10px] font-semibold">5th (Buddhi)</span>
              <strong className="text-primary font-bold">{h5.sign ? formatSignWithHindi(h5.sign) : 'Active'}</strong>
            </div>
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs">
              <span className="text-on-surface-variant block text-[10px] font-semibold">9th (Guru)</span>
              <strong className="text-primary font-bold">{h9.sign ? formatSignWithHindi(h9.sign) : 'Active'}</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Devanagari Classical Kalas Grid Card */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-4">
        <div className="flex items-center justify-between border-b border-outline-variant/40 pb-3">
          <h4 className="font-display text-lg font-bold text-primary flex items-center gap-2">
            <span className="material-symbols-outlined text-amber-500 text-xl">auto_awesome</span>
            Top Predicted Kalas (प्रमुख कलाएँ)
          </h4>
          <span className="text-xs font-bold text-primary bg-primary-fixed px-3 py-1 rounded-full border border-primary/20">
            64 Kalas (६४ कलाएँ)
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {top6Kalas.map((k, idx) => (
            <div
              key={idx}
              onClick={() => handleSelectKala(k.name)}
              className="bg-surface-variant/30 p-4 rounded-2xl border border-outline-variant/50 flex flex-col justify-between space-y-2 hover:border-primary/40 transition-all hover:bg-surface-variant/50 cursor-pointer shadow-xs group"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-extrabold text-amber-700 bg-amber-500/10 px-2 py-0.5 rounded-md border border-amber-500/20">
                  #{idx + 1} Kala
                </span>
                <span className="text-[11px] font-bold text-primary flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                  Explore <span className="material-symbols-outlined text-xs">arrow_downward</span>
                </span>
              </div>

              <div>
                <h5 className="font-display text-lg font-bold text-primary leading-tight">
                  {k.name}
                </h5>
                <p className="text-xs font-semibold text-amber-700 mt-1">
                  {k.devanagari}
                </p>
                <p className="text-[11px] text-on-surface-variant/80 mt-0.5 italic">
                  {k.meaning}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Interactive Kala Explorer Card with Dropdown */}
      <div
        ref={explorerRef}
        className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-5 scroll-mt-6"
      >
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-outline-variant/40 pb-4">
          <div>
            <h4 className="font-display text-xl font-bold text-primary flex items-center gap-2">
              <span className="material-symbols-outlined text-amber-600 text-2xl">menu_book</span>
              Interactive 64 Kalas Explorer (६४ कला खोजक एवं विस्तृत विवरण)
            </h4>
            <p className="text-xs text-on-surface-variant mt-0.5">
              Select any of the 64 Classical Kalas to read modern real-world examples, mastery methods, and horoscope alignment reasons.
            </p>
          </div>

          <div className="w-full sm:w-auto">
            <select
              value={selectedKalaName}
              onChange={(e) => handleSelectKala(e.target.value)}
              className="w-full sm:w-80 bg-surface-variant/60 text-primary border border-outline-variant/80 rounded-2xl px-4 py-2.5 text-xs font-bold shadow-xs focus:ring-2 focus:ring-primary focus:outline-none cursor-pointer"
            >
              {ALL_64_KALAS_RULES.map((k, idx) => (
                <option key={idx} value={k.name} className="bg-surface text-on-surface text-xs font-medium py-1">
                  {idx + 1}. {k.name} ({k.devanagari}) — {k.meaning}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Selected Kala Detailed Breakdown Card */}
        {selectedKalaEval && (
          <div className="bg-surface-variant/30 p-5 rounded-2xl border border-outline-variant/60 space-y-4 animate-fade-in-up">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-outline-variant/40 pb-3">
              <div>
                <span className="text-[10px] font-extrabold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                  Selected Classical Kala
                </span>
                <h5 className="font-display text-2xl font-bold text-primary mt-1">
                  {selectedKalaEval.name} <span className="text-lg font-semibold text-on-surface-variant">({selectedKalaEval.devanagari})</span>
                </h5>
                <p className="text-xs font-bold text-amber-800 mt-0.5">
                  {selectedKalaEval.meaning}
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <div className="bg-surface-variant/60 border border-outline-variant/40 px-3 py-1.5 rounded-xl text-xs">
                  <span className="text-on-surface-variant text-[10px] block font-semibold">Primary Houses</span>
                  <strong className="text-primary">{selectedKalaEval.houses.join(', ')}th Houses</strong>
                </div>
                <div className="bg-surface-variant/60 border border-outline-variant/40 px-3 py-1.5 rounded-xl text-xs">
                  <span className="text-on-surface-variant text-[10px] block font-semibold">Planetary Drivers</span>
                  <strong className="text-primary capitalize">{selectedKalaEval.planets.join(', ')}</strong>
                </div>
              </div>
            </div>

            {/* Horoscope Association & Astrological Reason Card */}
            <div className={`p-4 rounded-xl border text-xs font-medium space-y-1 ${
              selectedKalaEval.isTopAligned
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-900'
                : 'bg-amber-500/10 border-amber-500/30 text-amber-900'
            }`}>
              <div className="flex items-center gap-2 font-bold text-sm">
                <span className="material-symbols-outlined text-base">
                  {selectedKalaEval.isTopAligned ? 'stars' : 'balance'}
                </span>
                <h6>Horoscope Association & Astrological Reason</h6>
              </div>
              <p className="leading-relaxed">
                {selectedKalaEval.reasonSummary}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-surface p-4 rounded-xl border border-outline-variant/40 space-y-1.5">
                <div className="flex items-center gap-2 text-primary font-bold text-sm">
                  <span className="material-symbols-outlined text-amber-600 text-lg">work</span>
                  <h6>Modern Real-World Examples & Applications</h6>
                </div>
                <p className="text-xs text-on-surface-variant leading-relaxed">
                  {selectedKalaEval.examples}
                </p>
              </div>

              <div className="bg-surface p-4 rounded-xl border border-outline-variant/40 space-y-1.5">
                <div className="flex items-center gap-2 text-primary font-bold text-sm">
                  <span className="material-symbols-outlined text-emerald-600 text-lg">psychology</span>
                  <h6>How to Practice & Master this Vidya/Kala</h6>
                </div>
                <p className="text-xs text-on-surface-variant leading-relaxed">
                  {selectedKalaEval.masteryMethod}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Student Receptivity Pillars Grid */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-5">
        <div className="flex items-center justify-between border-b border-outline-variant/40 pb-3">
          <div>
            <h4 className="font-display text-lg font-bold text-primary flex items-center gap-2">
              <span className="material-symbols-outlined text-emerald-600 text-xl">psychology</span>
              Student Receptivity Pillars
            </h4>
            <p className="text-xs text-on-surface-variant mt-0.5">
              Horoscope astrological cognitive analysis & custom study retention strategy per pillar.
            </p>
          </div>

          <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full border border-emerald-300">
            Student Receptivity
          </span>
        </div>

        {/* 4 Receptivity Cards showing Calculated Receptivity Power */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {receptivityPillars.map((p, idx) => {
            const power = getReceptivityPower(p.name)
            return (
              <div
                key={idx}
                className="p-5 rounded-2xl border bg-surface-variant/30 border-outline-variant/50 hover:border-emerald-500/30 transition-all flex flex-col justify-between gap-3"
              >
                <div className="flex items-start gap-3.5">
                  <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-700 border border-emerald-500/20 flex items-center justify-center shrink-0 mt-0.5">
                    <span className="material-symbols-outlined text-xl">{p.icon}</span>
                  </div>
                  <div className="space-y-1 w-full">
                    <h5 className="font-display text-[15px] font-bold text-primary">
                      {p.devanagari}
                    </h5>
                    <p className="text-xs font-semibold text-emerald-800">
                      {p.title}
                    </p>
                    <p className="text-xs text-on-surface-variant/90 mt-1 leading-relaxed">
                      {p.desc}
                    </p>
                  </div>
                </div>

                <div className="flex flex-wrap items-center justify-between gap-2 border-t border-outline-variant/40 pt-3 mt-1">
                  <div className="text-xs font-bold text-emerald-800 bg-emerald-500/10 px-2.5 py-1 rounded-xl">
                    Receptivity Power: {power.score}% ({power.level})
                  </div>
                  <span className="text-[10px] text-on-surface-variant/80 italic">
                    Vedic Engine
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
