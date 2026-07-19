import { useState } from 'react'
import type { RelationshipType } from '../../types/profile'

interface BirthDetailsFormProps {
  onSubmit: (data: BirthData) => void
}

export interface BirthData {
  fullName: string
  gender: 'male' | 'female' | 'other'
  dateOfBirth: string
  timeOfBirth: string
  relationship?: RelationshipType
}

export default function BirthDetailsForm({ onSubmit }: BirthDetailsFormProps) {
  const [name, setName] = useState('')
  const [gender, setGender] = useState<'male' | 'female' | 'other'>('male')
  const [relationship, setRelationship] = useState<RelationshipType>('Self')
  const [dob, setDob] = useState('')
  const [tob, setTob] = useState('')

  const handleSubmit = () => {
    if (name && dob && tob) {
      onSubmit({ fullName: name, gender, dateOfBirth: dob, timeOfBirth: tob, relationship })
    }
  }

  const genderOptions: Array<{ value: 'male' | 'female' | 'other'; label: string }> = [
    { value: 'male', label: 'Male' },
    { value: 'female', label: 'Female' },
    { value: 'other', label: 'Other' },
  ]

  const relationshipOptions: RelationshipType[] = [
    'Self',
    'Spouse',
    'Child',
    'Parent',
    'Friend',
    'Other',
  ]

  return (
    <div className="ml-12 celestial-card rounded-3xl p-6 animate-fade-in-up">
      <h3 className="font-display text-[28px] leading-9 font-semibold mb-6 text-primary">
        Your Birth Essence
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Full Name */}
        <div className="space-y-1">
          <label className="text-[14px] leading-5 tracking-wide font-medium text-on-surface-variant px-1">
            Full Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Arjun Sharma"
            className="w-full bg-background border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:border-primary transition-all outline-none"
          />
        </div>

        {/* Relationship Tag */}
        <div className="space-y-1">
          <label className="text-[14px] leading-5 tracking-wide font-medium text-on-surface-variant px-1">
            Profile Relationship
          </label>
          <select
            value={relationship}
            onChange={(e) => setRelationship(e.target.value as RelationshipType)}
            className="w-full bg-background border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:border-primary transition-all outline-none cursor-pointer"
          >
            {relationshipOptions.map((rel) => (
              <option key={rel} value={rel}>
                {rel === 'Self' ? 'Self (My Chart)' : rel}
              </option>
            ))}
          </select>
        </div>

        {/* Gender */}
        <div className="space-y-1 md:col-span-2">
          <label className="text-[14px] leading-5 tracking-wide font-medium text-on-surface-variant px-1">
            Gender
          </label>
          <div className="flex gap-2">
            {genderOptions.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setGender(opt.value)}
                className={`flex-1 py-3 px-2 rounded-xl text-[14px] leading-5 tracking-wide font-medium transition-colors cursor-pointer ${
                  gender === opt.value
                    ? 'bg-primary text-on-primary'
                    : 'bg-background border border-outline-variant text-on-surface-variant hover:bg-primary-fixed hover:text-primary'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Date of Birth */}
        <div className="space-y-1">
          <label className="text-[14px] leading-5 tracking-wide font-medium text-on-surface-variant px-1">
            Date of Birth
          </label>
          <input
            type="date"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
            className="w-full bg-background border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary outline-none transition-all cursor-pointer"
          />
        </div>

        {/* Time of Birth */}
        <div className="space-y-1">
          <label className="text-[14px] leading-5 tracking-wide font-medium text-on-surface-variant px-1">
            Time of Birth
          </label>
          <input
            type="time"
            value={tob}
            onChange={(e) => setTob(e.target.value)}
            className="w-full bg-background border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary outline-none transition-all cursor-pointer"
          />
        </div>
      </div>

      <button
        onClick={handleSubmit}
        className="mt-8 w-full py-4 bg-gradient-to-r from-primary to-primary-container text-on-primary font-display text-[28px] leading-9 font-semibold rounded-2xl shadow-lg shadow-primary/20 hover:scale-[1.01] active:scale-95 transition-all cursor-pointer"
      >
        Continue →
      </button>
    </div>
  )
}
