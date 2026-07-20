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
}

const ALL_64_KALAS_RULES: ClassicalKalaRule[] = [
  { name: 'Gīta vidyā', devanagari: 'गीतविद्या', meaning: 'Vocal Music & Singing', houses: [2, 3, 5], planets: ['venus', 'mercury', 'moon'] },
  { name: 'Vādya vidyā', devanagari: 'वाद्यविद्या', meaning: 'Instrumental Music', houses: [3, 5], planets: ['venus', 'mercury', 'mars'] },
  { name: 'Nṛtya vidyā', devanagari: 'नृत्यविद्या', meaning: 'Dance & Movement', houses: [3, 5, 1], planets: ['venus', 'mars'] },
  { name: 'Nāṭya vidyā', devanagari: 'नाट्यविद्या', meaning: 'Theatrical Acting & Drama', houses: [3, 5, 10], planets: ['venus', 'rahu', 'mercury'] },
  { name: 'Ālekhya vidyā', devanagari: 'आलेख्यविद्या', meaning: 'Painting & Fine Arts', houses: [3, 4, 5], planets: ['venus', 'moon'] },
  { name: 'Viśeṣaka-cchēdya vidyā', devanagari: 'विशेषकच्छेद्यविद्या', meaning: 'Body Decoration & Cosmetology', houses: [1, 3], planets: ['venus', 'mercury'] },
  { name: 'Tāṇḍula-kusuma-balivikāra', devanagari: 'ताण्डुलकुसुमबलिविकार', meaning: 'Preparing Sacred Offerings', houses: [5, 9], planets: ['jupiter', 'sun'] },
  { name: 'Puṣpastaraṇa', devanagari: 'पुष्पास्तरण', meaning: 'Floral Bed & Spatial Design', houses: [4, 12], planets: ['venus', 'moon'] },
  { name: 'Danta-vasanāṅga-rāga', devanagari: 'दन्तवसनाङ्गराग', meaning: 'Perfumes & Hygiene Products', houses: [2, 6], planets: ['venus', 'mercury'] },
  { name: 'Maṇi-bhūmikā-karma', devanagari: 'मणिभूमिकाकर्म', meaning: 'Jewel Settings & Gemology', houses: [2, 3, 11], planets: ['sun', 'venus', 'mars'] },
  { name: 'Śayyā-racana', devanagari: 'शय्यारचन', meaning: 'Arranging Bedding & Comfort', houses: [4, 12], planets: ['venus', 'moon'] },
  { name: 'Udaka-vādya', devanagari: 'उदकवाद्य', meaning: 'Acoustic Music with Water', houses: [3, 4], planets: ['moon', 'venus'] },
  { name: 'Udaka-ghāta', devanagari: 'उदकघात', meaning: 'Water Hydraulics & Splashing Sports', houses: [4, 5], planets: ['moon', 'mars'] },
  { name: 'Citra-yoga', devanagari: 'चित्रयोग', meaning: 'Pigment & Color Formulation', houses: [3, 5], planets: ['mercury', 'venus'] },
  { name: 'Mālya-grathana-vikalpa', devanagari: 'माल्यग्रथनविकल्प', meaning: 'Floral Garland Synthesis', houses: [3, 5], planets: ['venus', 'mercury'] },
  { name: 'Śekharāpīḍa-yojana', devanagari: 'शेखरापीडयोजन', meaning: 'Coronet & Crown Crafting', houses: [1, 10], planets: ['sun', 'venus'] },
  { name: 'Nēpathyayoga', devanagari: 'नेपथ्ययोग', meaning: 'Costume & Fashion Design', houses: [3, 10], planets: ['venus', 'rahu'] },
  { name: 'Karṇapātra-bhaṅga', devanagari: 'कर्णपत्रभङ्ग', meaning: 'Ear Ornament Carving', houses: [3, 2], planets: ['venus', 'mercury'] },
  { name: 'Sugandha-yukti', devanagari: 'सुगन्धयुक्ति', meaning: 'Perfumery & Fragrance Synthesis', houses: [2, 5], planets: ['venus', 'jupiter'] },
  { name: 'Bhūṣaṇa-yojana', devanagari: 'भूषणयोजन', meaning: 'Ornamentation & Jewelry Styling', houses: [2, 1], planets: ['venus', 'sun'] },
  { name: 'Aindra-jāla', devanagari: 'ऐन्द्रजाल', meaning: 'Illusion, Magic & Sleight of Hand', houses: [3, 5, 8], planets: ['rahu', 'mercury'] },
  { name: 'Kaucumāra', devanagari: 'कौचुमार', meaning: 'Esoteric & Mystic Arts', houses: [8, 12], planets: ['ketu', 'jupiter'] },
  { name: 'Hasta-lāghava', devanagari: 'हस्तलाघव', meaning: 'Manual Precision & Fine Mechanics', houses: [3], planets: ['mercury', 'mars'] },
  { name: 'Citra-śākā-pūpa-bhakṣya-vikāra-kriyā', devanagari: 'चित्रशाकापूपभक्ष्यविकारक्रिया', meaning: 'Gourmet Culinary Arts', houses: [2, 4], planets: ['moon', 'venus', 'mars'] },
  { name: 'Pānaka-rasa-rāgāsava-yojana', devanagari: 'पानकरसरागासवयोजन', meaning: 'Mixology & Beverage Crafting', houses: [2, 5], planets: ['moon', 'venus'] },
  { name: 'Sūci-vāya-karma', devanagari: 'सूचिवायकर्म', meaning: 'Needlework, Embroidery & Weaving', houses: [3], planets: ['venus', 'mercury'] },
  { name: 'Sūtra-kṛīḍā', devanagari: 'सूत्रक्रीडा', meaning: 'Puppetry & String Mechanics', houses: [3, 5], planets: ['mercury', 'rahu'] },
  { name: 'Vīṇā-ḍamaruka-vādya', devanagari: 'वीणाडमरुकवाद्य', meaning: 'String Instrument & Percussion', houses: [3, 5], planets: ['venus', 'mars'] },
  { name: 'Prahelikā', devanagari: 'प्रहेलिका', meaning: 'Riddles & Logic Puzzles', houses: [5], planets: ['mercury', 'ketu'] },
  { name: 'Durvacaka-yoga', devanagari: 'दुर्वचकयोग', meaning: 'Cryptography & Conundrums', houses: [2, 5], planets: ['mercury', 'rahu'] },
  { name: 'Pustaka-vācana', devanagari: 'पुस्तकवाचन', meaning: 'Literary Recitation & Reading', houses: [2, 4, 5], planets: ['mercury', 'jupiter'] },
  { name: 'Nāṭikā-khyāyikā-darśana', devanagari: 'नाटिकाख्यायिकादर्शन', meaning: 'Storytelling & Enactment', houses: [3, 5], planets: ['mercury', 'moon'] },
  { name: 'Kāvya-samasya-pūraṇa', devanagari: 'काव्यसमस्यापूरण', meaning: 'Poetic Verse Composition', houses: [2, 5], planets: ['venus', 'jupiter', 'mercury'] },
  { name: 'Paṭṭikā-vetra-bāṇa-vikalpa', devanagari: 'पट्टिकावेत्रबाणविकल्प', meaning: 'Weapons, Armor & Shield Crafting', houses: [3, 6], planets: ['mars', 'saturn'] },
  { name: 'Tarku-karma', devanagari: 'तर्कुकर्म', meaning: 'Spindle Spinning & Fiber Tech', houses: [3], planets: ['saturn', 'mercury'] },
  { name: 'Takṣaṇa', devanagari: 'तक्षण', meaning: 'Carpentry & Structural Woodwork', houses: [4, 3], planets: ['mars', 'saturn'] },
  { name: 'Vāstu-vidyā', devanagari: 'वास्तुविद्या', meaning: 'Architecture & Engineering', houses: [4, 10], planets: ['mars', 'saturn', 'venus'] },
  { name: 'Raupya-ratna-parīkṣā', devanagari: 'रौप्यरत्नपरीक्षा', meaning: 'Testing Gems & Metals', houses: [2, 5, 11], planets: ['sun', 'mercury', 'jupiter'] },
  { name: 'Dhātu-vāda', devanagari: 'धातुवाद', meaning: 'Metallurgy & Materials Science', houses: [3, 10], planets: ['mars', 'saturn'] },
  { name: 'Maṇi-rāga-jñāna', devanagari: 'मणिशरागज्ञान', meaning: 'Jewel Dyeing & Coloration', houses: [2, 5], planets: ['venus', 'sun'] },
  { name: 'Ākāra-jñāna', devanagari: 'आकारज्ञान', meaning: 'Mineralogy & Geology', houses: [4, 8], planets: ['saturn', 'mars'] },
  { name: 'Vṛkṣāyurveda-yoga', devanagari: 'वृक्षायुर्वेदयोग', meaning: 'Botany & Herbal Healing', houses: [4, 6], planets: ['mercury', 'jupiter', 'sun'] },
  { name: 'Meṣa-kukkuṭa-lāvaka-yuddha-vidhi', devanagari: 'मेषकुक्कुटलावकयुद्धविधि', meaning: 'Animal Behavior & Training', houses: [6], planets: ['mars', 'saturn'] },
  { name: 'Śuka-sārikā-pralāpana', devanagari: 'शुकसारिकाप्रलापन', meaning: 'Avian Speech Training', houses: [2, 3], planets: ['mercury', 'jupiter'] },
  { name: 'Utsādana', devanagari: 'उत्सादन', meaning: 'Massage Therapy & Hygiene', houses: [1, 6], planets: ['mars', 'venus'] },
  { name: 'Keśa-mārjana-kauśala', devanagari: 'केशमार्जनकौशल', meaning: 'Trichology & Hair Styling', houses: [1, 3], planets: ['venus', 'mercury'] },
  { name: 'Akṣara-muṣṭika-kathana', devanagari: 'अक्षरमुष्टिकाकथन', meaning: 'Sign Language & Gestures', houses: [3], planets: ['mercury'] },
  { name: 'Dhāraṇa-mātrikā', devanagari: 'धारणामात्रिका', meaning: 'Protective Amulets & Yantras', houses: [5, 9], planets: ['jupiter', 'ketu'] },
  { name: 'Deśa-bhāṣā-jñāna', devanagari: 'देशभाषाज्ञान', meaning: 'Linguistics & Regional Dialects', houses: [2, 3, 9], planets: ['mercury', 'jupiter'] },
  { name: 'Nirmiti-jñāna', devanagari: 'निर्मितिज्ञान', meaning: 'Predictive Science & Omens', houses: [5, 8, 9], planets: ['jupiter', 'ketu'] },
  { name: 'Yantra-mātrikā', devanagari: 'यन्त्रमात्रिका', meaning: 'Mechanics, Robotics & Systems', houses: [3, 5, 10], planets: ['saturn', 'mars', 'mercury', 'rahu'] },
  { name: 'Mlecchita-kutarka-vikalpa', devanagari: 'म्लेच्छितकुतर्कविकल्प', meaning: 'Foreign Logic & Debating', houses: [3, 6, 9], planets: ['mercury', 'rahu'] },
  { name: 'Saṁvācya', devanagari: 'संवाच्य', meaning: 'Oratory, Speech & Dialogue', houses: [2, 3, 10], planets: ['mercury', 'jupiter'] },
  { name: 'Mānasi kāvya-kriyā', devanagari: 'मानसी काव्यक्रिया', meaning: 'Mental Poetic Composition', houses: [5], planets: ['venus', 'moon', 'jupiter'] },
  { name: 'Kriyā-vikalpa', devanagari: 'क्रियाविकल्प', meaning: 'Therapeutic Design & Remedies', houses: [5, 6, 9], planets: ['jupiter', 'sun'] },
  { name: 'Calitaka-yoga', devanagari: 'चलितकयोग', meaning: 'Sacred Shrine Architecture', houses: [4, 9], planets: ['jupiter', 'saturn'] },
  { name: 'Abhidhāna-kośa-chanda-jñāna', devanagari: 'अभिधानकोशछन्दोज्ञान', meaning: 'Lexicography & Prosody', houses: [2, 5], planets: ['mercury', 'jupiter'] },
  { name: 'Vastra-gopana', devanagari: 'वस्त्रगोपन', meaning: 'Textile Concealment Art', houses: [3, 8], planets: ['venus', 'ketu'] },
  { name: 'Dyūta-viśeṣa', devanagari: 'द्यूतविशेष', meaning: 'Game Theory & Probability', houses: [5, 11], planets: ['mercury', 'rahu'] },
  { name: 'Ākarṣa-kṛīḍā', devanagari: 'आकर्षक्रीडा', meaning: 'Magnetics & Physics Play', houses: [3, 8], planets: ['mars', 'saturn'] },
  { name: 'Bālaka-kṛīḍanaka', devanagari: 'बालकक्रीडनक', meaning: 'Toy Crafting & Recreation', houses: [3, 5], planets: ['mercury', 'venus'] },
  { name: 'Vainayikī vidyā', devanagari: 'वैनायिकी विद्या', meaning: 'Pedagogy & Discipline', houses: [5, 9], planets: ['jupiter', 'sun'] },
  { name: 'Vaijayikī vidyā', devanagari: 'वैजयिकी विद्या', meaning: 'Military Strategy & Victory', houses: [6, 10], planets: ['mars', 'sun'] },
  { name: 'Vaitālikī vidyā', devanagari: 'वैतालिकी विद्या', meaning: 'Melodic Awakening Music', houses: [2, 3], planets: ['venus', 'moon'] },
]

export default function KalaVidyaDashboard({ chartData }: KalaVidyaDashboardProps) {
  const houses = chartData?.houses || {}
  const rawPositions = chartData?.raw_positions || chartData?.planets || {}
  const yogas = chartData?.yogas || []

  const h3 = houses['3'] || {}
  const h5 = houses['5'] || {}
  const h10 = houses['10'] || {}

  // Perform identical evaluation calculation as Python backend engine (kala_vidya_engine.py)
  const evaluatedKalas = ALL_64_KALAS_RULES.map((item) => {
    let score = 62

    // Evaluate target planets dynamically from user natal chart
    for (const pName of item.planets) {
      const pData =
        rawPositions[pName] ||
        rawPositions[pName.toLowerCase()] ||
        rawPositions[pName.charAt(0).toUpperCase() + pName.slice(1)]
      if (pData) {
        const dig = (pData.dignity || 'neutral').toLowerCase()
        const h = pData.house || 0
        if (dig === 'exalted' || dig === 'own') score += 8
        else if (dig === 'debilitated') score -= 8

        if (item.houses.includes(h)) score += 7
      }
    }

    // Evaluate house lords dynamically
    for (const hNum of item.houses) {
      const hInfo = houses[String(hNum)]
      if (hInfo && hInfo.lord && item.planets.includes(hInfo.lord.toLowerCase())) {
        score += 5
      }
    }

    if (yogas.length > 0) score += 5

    const finalScore = Math.max(40, Math.min(98, score))
    return {
      name: item.name,
      devanagari: item.devanagari,
      meaning: item.meaning,
      score: finalScore,
    }
  })

  // Sort by calculated score descending and pick top 6
  evaluatedKalas.sort((a, b) => b.score - a.score)
  const top6Kalas = evaluatedKalas.slice(0, 6)

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
                  ६४ चतुःषष्टि कला (64 Classical Vedic Kalas)
                </h3>
                <span className="text-[11px] font-extrabold bg-primary-fixed text-primary px-2.5 py-0.5 rounded-full">
                  Vedic Astrology Engine
                </span>
              </div>
              <p className="text-xs text-on-surface-variant font-medium mt-0.5">
                Predictive Devanagari Talent Mapping based on D1 Lagna, D10 Dashamsha & D24 Siddhamsha
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs">
              <span className="text-on-surface-variant block text-[10px] font-semibold">3rd House (Hands/Skills)</span>
              <strong className="text-primary font-bold">{h3.sign ? formatSignWithHindi(h3.sign) : 'Active'}</strong>
            </div>
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs">
              <span className="text-on-surface-variant block text-[10px] font-semibold">5th House (Intellect)</span>
              <strong className="text-primary font-bold">{h5.sign ? formatSignWithHindi(h5.sign) : 'Active'}</strong>
            </div>
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs">
              <span className="text-on-surface-variant block text-[10px] font-semibold">10th House (Karma)</span>
              <strong className="text-primary font-bold">{h10.sign ? formatSignWithHindi(h10.sign) : 'Active'}</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Devanagari Classical Kalas Grid Display */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-4">
        <div className="flex items-center justify-between border-b border-outline-variant/40 pb-3">
          <h4 className="font-display text-lg font-bold text-primary flex items-center gap-2">
            <span className="material-symbols-outlined text-amber-500 text-xl">auto_awesome</span>
            आपकी कुण्डली के अनुसार प्रमुख कलाएँ (Top Predicted Kalas in Devanagari)
          </h4>
          <span className="text-xs font-bold text-primary bg-primary-fixed px-3 py-1 rounded-full border border-primary/20">
            ६४ कलाएँ
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {top6Kalas.map((k, idx) => (
            <div
              key={idx}
              className="bg-surface-variant/30 p-4 rounded-2xl border border-outline-variant/50 flex flex-col justify-between space-y-2 hover:border-primary/40 transition-all hover:bg-surface-variant/50"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-extrabold text-amber-700 bg-amber-500/10 px-2 py-0.5 rounded-md border border-amber-500/20">
                  #{idx + 1} Kala
                </span>
              </div>

              <div>
                <h5 className="font-display text-xl font-bold text-primary leading-tight">
                  {k.devanagari}
                </h5>
                <p className="text-xs font-semibold text-on-surface mt-1">
                  {k.name}
                </p>
                <p className="text-[11px] text-on-surface-variant/80 mt-0.5 italic">
                  {k.meaning}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

