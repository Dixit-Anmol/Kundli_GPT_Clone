interface NavbarProps {
  profileImage?: string
}

export default function Navbar({ profileImage }: NavbarProps) {
  return (
    <nav className="glass border-b border-outline-variant/50 h-[72px] sticky top-0 z-50 flex items-center justify-between px-4 md:px-10">
      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-on-primary shadow-sm">
          <span className="material-symbols-outlined text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>
            auto_awesome
          </span>
        </div>
        <div>
          <h1 className="font-display text-[28px] leading-tight font-semibold text-primary">
            Kundli AI
          </h1>
          <p className="text-[12px] leading-4 font-semibold text-on-surface-variant">
            Horoscope Grounded AI Assistant
          </p>
        </div>
      </div>

      {/* Desktop Navigation */}
      <div className="hidden md:flex items-center gap-8">
        <a
          href="#"
          className="text-[14px] leading-5 tracking-wide font-medium text-primary border-b-2 border-primary pb-1"
        >
          New Chat
        </a>
        <a
          href="#"
          className="text-[14px] leading-5 tracking-wide font-medium text-on-surface-variant hover:text-primary transition-colors"
        >
          History
        </a>

        {/* Profile Avatar */}
        <div className="w-10 h-10 rounded-full overflow-hidden border border-outline-variant cursor-pointer hover:scale-105 transition-transform">
          {profileImage ? (
            <img src={profileImage} alt="Profile" className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full bg-primary-fixed flex items-center justify-center">
              <span className="material-symbols-outlined text-primary text-lg">person</span>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
