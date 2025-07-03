# HOT PPL: The Search - Main Trio Character Specifications

## Character Asset Requirements

This document outlines the specifications for the three main characters in HOT PPL: The Search. These characters form the core of the social adventure experience and should be designed to represent different archetypes and playstyles.

---

## 1. Minilambobae (Protagonist)
**Archetype:** Balanced Protagonist  
**Role:** Main playable character, social connector

### Physical Specifications
- **Height:** 5'6" (168cm) - Average height for versatility
- **Build:** Athletic but not overly muscular, approachable physique
- **Age Appearance:** Early 20s
- **Skin Tone:** Medium, with customization options for all ethnicities
- **Hair:** Shoulder-length, wavy, default dark brown (fully customizable)
- **Eyes:** Large, expressive, default hazel (fully customizable)

### Style Profile
- **Default Style:** Trendy casual with designer touches
- **Fashion Sense:** 75/100 - High but not intimidating
- **Personality:** Confident, friendly, adaptable
- **Signature Look:** Mix of streetwear and high fashion

### Default Outfit
- **Top:** Fitted graphic tee with subtle designer logo
- **Bottom:** High-waisted distressed jeans
- **Shoes:** Clean white sneakers with colored accents
- **Accessories:** Layered gold necklaces, small hoop earrings
- **Outerwear:** Cropped denim jacket

### Customization Options
- **Hair Styles:** 12+ options (short pixie to long waves)
- **Hair Colors:** Full spectrum including natural and fantasy colors
- **Skin Tones:** 8+ realistic options covering all ethnicities
- **Eye Colors:** 6+ natural colors plus colored contacts
- **Body Type:** Slight adjustments to proportions

### Animation Requirements
- **Idle:** Confident stance, occasional hair flip
- **Walk:** Purposeful stride with slight swagger
- **Talk:** Expressive hand gestures, engaging eye contact
- **Facial Expressions:** Wide range for social interactions

---

## 2. Aria Luxe (The Fashionista)
**Archetype:** Fashion Maven  
**Role:** Style guru, trendsetter, fashion district guide

### Physical Specifications
- **Height:** 5'8" (173cm) - Tall and statuesque
- **Build:** Slim, model-like proportions
- **Age Appearance:** Mid 20s
- **Skin Tone:** Pale with warm undertones (customizable)
- **Hair:** Long, straight, platinum blonde (signature look)
- **Eyes:** Striking blue with dramatic makeup

### Style Profile
- **Default Style:** High fashion, avant-garde
- **Fashion Sense:** 95/100 - Trendsetting expert
- **Personality:** Sophisticated, discerning, inspiring
- **Signature Look:** Designer everything, statement pieces

### Default Outfit
- **Top:** Silk blouse with dramatic sleeves
- **Bottom:** Tailored wide-leg trousers
- **Shoes:** Designer heels with unique silhouette
- **Accessories:** Statement earrings, designer handbag, multiple rings
- **Outerwear:** Structured blazer or designer coat

### Customization Options
- **Hair Styles:** 10+ high-fashion options
- **Hair Colors:** Focus on bold, fashion-forward colors
- **Makeup:** Dramatic options, editorial looks
- **Accessories:** Extensive high-end jewelry collection
- **Clothing:** Designer and avant-garde pieces

### Animation Requirements
- **Idle:** Poised stance, occasional pose adjustments
- **Walk:** Runway-style stride, confident posture
- **Talk:** Elegant gestures, expressive but controlled
- **Facial Expressions:** Sophisticated, evaluative looks

---

## 3. Kai Velocity (The Racer)
**Archetype:** Street Racer  
**Role:** Vehicle expert, underground scene connector

### Physical Specifications
- **Height:** 5'10" (178cm) - Tall and athletic
- **Build:** Lean muscle, athletic build
- **Age Appearance:** Early 20s
- **Skin Tone:** Olive complexion (customizable)
- **Hair:** Short, textured, dark with colored streaks
- **Eyes:** Dark brown, intense gaze

### Style Profile
- **Default Style:** Urban streetwear, racing-inspired
- **Fashion Sense:** 60/100 - Function over form, but stylish
- **Personality:** Confident, competitive, loyal
- **Signature Look:** Racing gear meets street fashion

### Default Outfit
- **Top:** Racing-inspired bomber jacket over fitted tee
- **Bottom:** Slim-fit cargo pants with technical details
- **Shoes:** High-performance sneakers
- **Accessories:** Racing gloves, chain necklace, smartwatch
- **Outerwear:** Leather jacket with racing patches

### Customization Options
- **Hair Styles:** 8+ short to medium styles
- **Hair Colors:** Natural colors plus racing-inspired streaks
- **Clothing:** Racing gear, streetwear, athletic wear
- **Accessories:** Racing-themed jewelry and gear
- **Tattoos:** Optional racing and automotive-themed designs

### Animation Requirements
- **Idle:** Relaxed but alert stance, occasional stretch
- **Walk:** Confident stride with slight bounce
- **Talk:** Animated gestures, enthusiastic expressions
- **Facial Expressions:** Competitive grins, focused concentration

---

## Technical Requirements

### Model Specifications
- **Polygon Count:** 15,000-25,000 triangles (optimized for real-time)
- **Texture Resolution:** 2048x2048 for main textures, 1024x1024 for accessories
- **Rigging:** Standard humanoid rig compatible with Unity's Humanoid system
- **Blend Shapes:** Minimum 20 facial blend shapes for expressions
- **LOD Levels:** 3 levels (High, Medium, Low detail)

### Clothing System
- **Modular Design:** Each clothing piece as separate mesh
- **Bone Weights:** Properly weighted to character skeleton
- **Material Variants:** Multiple color/pattern options per piece
- **Layering System:** Support for multiple clothing layers

### Facial Animation
- **Blend Shapes Required:**
  - Eye blink (left/right separate)
  - Mouth open/close
  - Smile variations
  - Eyebrow movements
  - Cheek puff
  - Jaw movement
  - Emotion sets (happy, sad, angry, surprised, etc.)

### File Organization
```
Assets/Art/Characters/
├── Models/
│   ├── Minilambobae/
│   │   ├── Minilambobae_Base.fbx
│   │   ├── Minilambobae_LOD1.fbx
│   │   ├── Minilambobae_LOD2.fbx
│   │   └── Textures/
│   ├── AriaLuxe/
│   │   ├── AriaLuxe_Base.fbx
│   │   ├── AriaLuxe_LOD1.fbx
│   │   ├── AriaLuxe_LOD2.fbx
│   │   └── Textures/
│   └── KaiVelocity/
│       ├── KaiVelocity_Base.fbx
│       ├── KaiVelocity_LOD1.fbx
│       ├── KaiVelocity_LOD2.fbx
│       └── Textures/
├── Clothing/
│   ├── Tops/
│   ├── Bottoms/
│   ├── Shoes/
│   ├── Accessories/
│   └── Outerwear/
└── Materials/
    ├── Skin/
    ├── Hair/
    ├── Eyes/
    └── Clothing/
```

### Performance Targets
- **Target FPS:** 60 FPS with all three characters on screen
- **Memory Usage:** <50MB total for all character assets
- **Draw Calls:** Minimize through texture atlasing and batching
- **Animation Performance:** Smooth 30+ FPS during facial animations

---

## Implementation Notes

1. **Unity Integration:** All models should import cleanly into Unity 2023.3 LTS
2. **Animation Compatibility:** Ensure compatibility with Unity's Humanoid animation system
3. **Customization System:** Design with the modular clothing system in mind
4. **Performance Optimization:** Use LOD system and texture compression
5. **Style Consistency:** Maintain visual cohesion across all three characters
6. **Cultural Sensitivity:** Ensure diverse representation and avoid stereotypes

This specification provides the foundation for creating the main trio characters that will drive the social adventure gameplay in HOT PPL: The Search.
