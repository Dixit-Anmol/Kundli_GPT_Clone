import { useState, useEffect } from 'react'

interface BirthplaceMapProps {
  onConfirm: (place: string, lat: number, lon: number) => void
}

interface Suggestion {
  place_id: number
  display_name: string
  lat: string
  lon: string
}

export default function BirthplaceMap({ onConfirm }: BirthplaceMapProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedPlace, setSelectedPlace] = useState('Mumbai, Maharashtra, India')
  const [coordinates, setCoordinates] = useState({ lat: 19.076, lon: 72.8777 })
  const [suggestions, setSuggestions] = useState<Suggestion[]>([])
  const [loading, setLoading] = useState(false)
  const [showDropdown, setShowDropdown] = useState(false)

  // Debounced geocoding search
  useEffect(() => {
    if (!searchQuery.trim() || searchQuery.length < 3) {
      setSuggestions([])
      setShowDropdown(false)
      return
    }

    const timer = setTimeout(async () => {
      setLoading(true)
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
            searchQuery
          )}&limit=5&addressdetails=1`,
          {
            headers: {
              'User-Agent': 'KundliGPT-VedicAstrology-Assistant',
            },
          }
        )
        if (response.ok) {
          const data: Suggestion[] = await response.json()
          setSuggestions(data)
          setShowDropdown(data.length > 0)
        }
      } catch (err) {
        console.error('Geocoding error:', err)
      } finally {
        setLoading(false)
      }
    }, 500)

    return () => clearTimeout(timer)
  }, [searchQuery])

  const handleSelectSuggestion = (s: Suggestion) => {
    setSelectedPlace(s.display_name)
    setCoordinates({ lat: parseFloat(s.lat), lon: parseFloat(s.lon) })
    setSearchQuery(s.display_name)
    setShowDropdown(false)
  }

  const handleConfirm = () => {
    onConfirm(selectedPlace, coordinates.lat, coordinates.lon)
  }

  // Calculate bbox for OpenStreetMap Export embed
  const offset = 0.015
  const bbox = `${coordinates.lon - offset}%2C${coordinates.lat - offset}%2C${
    coordinates.lon + offset
  }%2C${coordinates.lat + offset}`
  const mapSrc = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${coordinates.lat}%2C${coordinates.lon}`

  return (
    <div className="ml-12 celestial-card rounded-3xl overflow-hidden animate-fade-in-up delay-200">
      {/* Map Area */}
      <div className="relative h-64 w-full bg-surface-variant/40">
        {/* Dynamic OpenStreetMap Embed Iframe */}
        <iframe
          title="Birthplace Map"
          src={mapSrc}
          className="w-full h-full border-none opacity-90 transition-opacity duration-300"
          loading="lazy"
        />

        {/* Search Overlay */}
        <div className="absolute top-4 left-4 right-4 z-20">
          <div className="relative">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">
              {loading ? 'sync' : 'search'}
            </span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search birth city..."
              className="w-full pl-10 pr-4 py-3 glass border border-white/60 rounded-xl shadow-lg focus:outline-none placeholder:text-on-surface-variant/60 text-on-surface"
              onFocus={() => {
                if (suggestions.length > 0) setShowDropdown(true)
              }}
            />

            {/* Autocomplete Dropdown */}
            {showDropdown && (
              <div className="absolute left-0 right-0 mt-2 bg-white/95 backdrop-blur-md border border-outline-variant rounded-xl shadow-xl max-h-48 overflow-y-auto z-30 divide-y divide-outline-variant/30">
                {suggestions.map((s) => (
                  <button
                    key={s.place_id}
                    onClick={() => handleSelectSuggestion(s)}
                    className="w-full px-4 py-2.5 text-left text-[13px] hover:bg-primary-fixed hover:text-primary transition-colors text-on-surface line-clamp-1"
                  >
                    {s.display_name}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Subtle Map Pin overlay for visuals (aligned center) */}
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center z-10">
          <div className="w-10 h-10 bg-primary/20 rounded-full animate-ping absolute" />
          <span
            className="material-symbols-outlined text-primary text-4xl relative z-10 -translate-y-2"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            location_on
          </span>
        </div>
      </div>

      {/* Confirm Bar */}
      <div className="p-6 flex items-center justify-between bg-surface relative z-10 border-t border-outline-variant/40">
        <span className="text-[14px] leading-5 tracking-wide font-medium text-on-surface max-w-[65%] line-clamp-1">
          {selectedPlace}
        </span>
        <button
          onClick={handleConfirm}
          className="px-6 py-2 bg-primary text-on-primary rounded-full text-[14px] leading-5 tracking-wide font-medium hover:bg-primary-container transition-colors shadow-sm cursor-pointer"
        >
          Confirm Birthplace
        </button>
      </div>
    </div>
  )
}
