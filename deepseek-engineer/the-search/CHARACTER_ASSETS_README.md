# HOT PPL: The Search - Character Assets System

## Overview

This document outlines the complete character asset system for the main trio in HOT PPL: The Search. The system provides a comprehensive foundation for character customization, facial animation, and modular clothing that supports the game's social adventure gameplay.

## Main Trio Characters

### 1. **Minilambobae** (Protagonist)
- **Role:** Main playable character, social connector
- **Style:** Trendy casual with designer touches
- **Stats:** Balanced across all areas (Social: 75, Fashion: 75, Driving: 65, Charisma: 80)
- **Customization:** Full range of options for player expression

### 2. **Aria Luxe** (The Fashionista)
- **Role:** Fashion expert, style evaluator
- **Style:** High fashion, avant-garde
- **Stats:** Fashion-focused (Social: 85, Fashion: 95, Driving: 45, Charisma: 90)
- **Customization:** Emphasis on high-fashion options

### 3. **Kai Velocity** (The Racer)
- **Role:** Vehicle expert, street racing guide
- **Style:** Urban streetwear, racing-inspired
- **Stats:** Driving-focused (Social: 65, Fashion: 60, Driving: 95, Charisma: 75)
- **Customization:** Athletic and racing-themed options

## System Architecture

### Core Scripts

1. **CharacterData.cs** - Scriptable Object defining character properties
2. **CharacterCustomization.cs** - Real-time character customization system
3. **ClothingSystem.cs** - Modular clothing and accessory management
4. **FacialAnimationController.cs** - Facial expressions and lip sync
5. **CharacterAssetSetup.cs** - Setup and validation tools

### Asset Structure

```
Assets/
├── Scripts/Character/          # Character system scripts
├── Art/Characters/            # 3D models, textures, materials
│   ├── Models/               # Character meshes (.fbx files)
│   ├── Textures/            # Character textures
│   ├── Materials/           # Unity materials
│   └── Animations/          # Facial animation data
├── Art/Clothing/             # Modular clothing assets
│   ├── Tops/               # Shirt, blouse, jacket meshes
│   ├── Bottoms/            # Pants, skirts, shorts meshes
│   ├── Shoes/              # Footwear meshes
│   ├── Accessories/        # Jewelry, bags, etc.
│   └── Outerwear/          # Coats, jackets
├── Prefabs/Characters/       # Character prefab templates
├── Data/Characters/          # Character data assets
├── Data/Clothing/           # Clothing item definitions
└── Data/Accessories/        # Accessory item definitions
```

## Key Features

### Character Customization System
- **Modular Design:** Swap clothing, accessories, hair, and colors in real-time
- **Style Evaluation:** Automatic scoring based on fashion sense and style synergy
- **Archetype Compatibility:** Different items suit different character types
- **Save/Load System:** Persistent customization across game sessions

### Facial Animation System
- **Blend Shape Control:** 20+ facial expressions using blend shapes
- **Automatic Lip Sync:** Real-time lip sync with voice audio
- **Eye Movement:** Subtle eye tracking and blinking
- **Expression Library:** Pre-defined expressions for different emotions

### Clothing System
- **Slot-Based:** Organized by clothing slots (Top, Bottom, Shoes, etc.)
- **Material Variants:** Multiple color/pattern options per item
- **Style Properties:** Each item has fashion, casual, formal, and street values
- **Unlock System:** Progressive unlocking based on player progression

## Technical Specifications

### Performance Targets
- **Polygon Count:** 15,000-25,000 triangles per character
- **Texture Resolution:** 2048x2048 for main textures, 1024x1024 for accessories
- **Frame Rate:** 60 FPS with all three characters on screen
- **Memory Usage:** <50MB total for all character assets

### Unity Integration
- **Unity Version:** 2023.3 LTS
- **Render Pipeline:** Universal Render Pipeline (URP)
- **Animation System:** Humanoid rigs with Unity's animation system
- **Audio System:** 3D spatial audio for voice and lip sync

## Implementation Status

### ✅ Completed
- Core character system architecture
- Character data structure and scriptable objects
- Modular clothing and accessory system
- Facial animation framework
- Character customization system
- Style evaluation mechanics
- Setup and validation tools

### 🔄 In Progress
- 3D character models (requires 3D artist)
- Texture and material creation
- Clothing item meshes
- Animation controllers
- Audio integration

### 📋 Next Steps
1. **3D Asset Creation:** Create actual character models following the specifications
2. **Texture Development:** Design and create character textures and materials
3. **Clothing Meshes:** Model modular clothing pieces
4. **Animation Setup:** Configure animation controllers and blend shapes
5. **Testing:** Validate system with real assets
6. **Optimization:** Performance tuning and LOD implementation

## Usage Instructions

### For Developers
1. **Setup:** Run `CharacterAssetSetup.SetupCharacterAssets()` to initialize the system
2. **Testing:** Use `CharacterAssetSetup.CreateTestScene()` to spawn all three characters
3. **Validation:** The setup script will validate all character data and report issues

### For 3D Artists
1. **Reference:** Use `MainTrio_CharacterSpecs.md` for detailed character specifications
2. **Standards:** Follow Unity humanoid rigging standards
3. **Optimization:** Keep polygon counts within specified limits
4. **Integration:** Import models and configure as specified in the documentation

### For Designers
1. **Clothing Items:** Create new clothing using the ClothingItem scriptable object
2. **Style Tuning:** Adjust fashion values and style properties
3. **Character Stats:** Modify character base stats in CharacterData assets

## Style System

The style evaluation system scores outfits based on:
- **Fashion Value:** Overall fashionability of items
- **Style Synergy:** Bonus for matching style types
- **Character Compatibility:** Items suited to character archetypes
- **Situation Appropriateness:** Casual vs formal vs street contexts

## Facial Animation

The facial animation system supports:
- **Automatic Expressions:** Context-appropriate facial expressions
- **Manual Control:** Direct expression changes via script
- **Lip Sync:** Real-time mouth movement with audio
- **Eye Tracking:** Subtle eye movement and blinking
- **Blend Shape Library:** Comprehensive set of facial controls

## Future Enhancements

### Planned Features
- **Body Type Variations:** Different body shapes and sizes
- **Makeup System:** Cosmetic customization options
- **Tattoo System:** Custom tattoo placement and design
- **Hair Physics:** Dynamic hair movement and physics
- **Clothing Physics:** Cloth simulation for flowing garments

### Technical Improvements
- **LOD System:** Automatic level-of-detail switching
- **Texture Streaming:** Dynamic texture loading for memory optimization
- **Animation Compression:** Optimized animation data storage
- **Mobile Optimization:** Platform-specific optimizations

## Support and Documentation

- **Character Specifications:** See `MainTrio_CharacterSpecs.md`
- **Setup Guide:** Use `CharacterAssetSetup.cs` for automated setup
- **Technical Reference:** Inline code documentation in all scripts
- **Asset Creation:** Follow guidelines in generated documentation

This character asset system provides a solid foundation for the social adventure gameplay in HOT PPL: The Search, supporting the game's emphasis on style, customization, and character expression.
