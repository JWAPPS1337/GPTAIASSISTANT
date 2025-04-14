import React from 'react'

interface ChatbotUISVGProps {
  theme?: 'light' | 'dark'
  scale?: number
}

export const ChatbotUISVG: React.FC<ChatbotUISVGProps> = ({ 
  theme = 'light',
  scale = 1 
}) => {
  const color = theme === 'dark' ? '#FFFFFF' : '#000000'
  
  return (
    <svg 
      width={200 * scale} 
      height={200 * scale} 
      viewBox="0 0 200 200" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Main circle (head) */}
      <circle 
        cx="100" 
        cy="100" 
        r="80" 
        stroke={color} 
        strokeWidth="8" 
        fill="none"
      />
      
      {/* Eyes */}
      <circle 
        cx="70" 
        cy="80" 
        r="10" 
        fill={color}
      />
      <circle 
        cx="130" 
        cy="80" 
        r="10" 
        fill={color}
      />
      
      {/* Smile */}
      <path
        d="M60 120 Q100 150 140 120"
        stroke={color}
        strokeWidth="8"
        fill="none"
      />
      
      {/* Antenna */}
      <line 
        x1="100" 
        y1="20" 
        x2="100" 
        y2="0" 
        stroke={color} 
        strokeWidth="8"
      />
      <circle 
        cx="100" 
        cy="0" 
        r="4" 
        fill={color}
      />
    </svg>
  )
} 