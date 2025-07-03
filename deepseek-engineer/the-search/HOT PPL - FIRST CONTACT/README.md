# HOT PPL - FIRST CONTACT
## Unity 6.2 Vehicle System

A Unity vehicle system featuring three alien visitors in chrome and black Lamborghinis searching for Earth's "hot people" but finding only disappointing archetypes.

## Characters

### Main Squad (Alien Visitors)
- **MINILAMBOBAE** (Player Character) - Drives ARCHIE, the chrome Lamborghini with AI personality
- **BECCA** (AI Teammate) - Analytical skeptic in black Lamborghini, predicted mission failure
- **JENNY** (AI Teammate) - Eternal optimist in black Lamborghini, refuses to give up hope

### Vehicle AI
- **ARCHIE** - Chrome Lamborghini AI with advanced humor and commentary system:
  - **Dynamic mood system**: Starts optimistic, becomes increasingly disappointed
  - **Contextual reactions**: Responds to driving, crashes, parking, and mission events
  - **Running gag system**: Recurring jokes that build throughout the experience
  - **Earth culture confusion**: Misunderstands human customs with funny results
  - **Sarcastic responses**: Reacts to player actions with witty commentary
  - **Voice line triggers**: Event-based dialogue for immersive experience

### Disappointing Male Archetypes
- **Discount Diplo** - Terrible DJ with delusions of grandeur
- **Tracksuit Guy** - Crypto bro with fake wealth and bad pickup lines
- **Finance Bro** - Trust fund kid showing off meaningless possessions
- **Mafia Guy** - Harmless wannabe tough guy from too many movies

## Features

### Vehicle System
- **Arcade-style driving controls** (WASD/Arrow keys/Touch/Gamepad)
- **Chrome Lamborghini** (ARCHIE) - Player vehicle with AI personality
- **Two black Lamborghinis** (Becca & Jenny) - AI-controlled followers
- **Auto-park system** at nightclub destination
- **Simple traffic system** with basic AI vehicles

### Opening Cutscene
- Three Lamborghinis descending from space
- Multiple camera angles during atmospheric entry
- Landing sequence in the city
- Particle effects for space and landing

### Character Interactions
- **ARCHIE** provides dynamic humor system with:
  - Mood-based commentary (6 different mood states)
  - Contextual reactions to game events
  - Running gags that evolve throughout gameplay
  - Sarcastic responses to player mistakes
  - Earth culture misunderstandings
- **MINILAMBOBAE** scans for specimens with increasing disappointment
- **BECCA** offers analytical insights and reality checks
- **JENNY** maintains optimism and suggests distractions

### Archetype Encounters
- Proximity-based detection system
- Character-specific reactions to each archetype
- Dialogue system with personality-appropriate responses
- Mini-games for archetype interactions (planned)

## Setup Instructions

### Unity 6.2 Requirements
1. Open Unity Hub
2. Install Unity 6.2.0f1 or later
3. Create new 3D project or open existing project
4. Import the HOT PPL - FIRST CONTACT assets

### Scene Setup
1. Create a new scene or use the provided scene
2. Add the `SceneSetupManager` script to an empty GameObject
3. Configure the following in the inspector:

#### Vehicle Prefabs
- Assign Lamborghini prefabs for ARCHIE (chrome), BECCA (black), JENNY (black)
- Ensure each prefab has appropriate colliders and Rigidbody components

#### Spawn Positions
- Set ground-level spawn positions for each vehicle
- Position them in formation (ARCHIE center, BECCA left, JENNY right)

#### Cutscene Positions
- **Space Start Positions**: High altitude positions (Y > 100)
- **Landing Positions**: Final ground positions after cutscene
- **Camera Positions**: Multiple angles for dramatic cutscene

#### Environment
- **Nightclub Location**: Destination for auto-park system
- **Parking Spots**: Designated parking positions (3 spots minimum)
- **Waypoint Route**: Path for traffic system

### Input System Setup
1. Install Input System package via Package Manager
2. Import the `VehicleInputActions.inputactions` asset
3. Assign to PlayerInput component on ARCHIE vehicle

### Audio Setup
- Add AudioSource components to vehicles
- Assign engine sounds, voice clips, and effect sounds
- Configure 3D spatial audio settings

### UI Setup
1. Create Canvas for gameplay UI
2. Add Text components for character dialogue
3. Create scanning UI with progress bars
4. Setup cutscene UI with title and subtitle text

## Controls

### Keyboard
- **W/S or Up/Down**: Accelerate/Reverse
- **A/D or Left/Right**: Steering
- **Space**: Brake
- **Space** (when stationary): Scan for specimens

### Touch (Mobile)
- **Touch and drag**: Steering and acceleration
- **Tap and hold**: Brake
- **Single tap**: Scan for specimens

### Gamepad
- **Left stick**: Steering and acceleration
- **A button**: Brake
- **A button** (when stationary): Scan for specimens

## Script Overview

### Core Vehicle Scripts
- `VehicleController.cs` - Main player vehicle physics and controls
- `AIFollowerVehicle.cs` - AI vehicles that follow the player
- `ArchiePersonality.cs` - AI commentary system for the chrome Lamborghini

### Character Scripts
- `MinilambobaeController.cs` - Player character with scanning system
- `BeccaController.cs` - Analytical AI teammate with research data
- `JennyController.cs` - Optimistic AI teammate with distraction abilities

### Game Systems
- `OpeningCutscene.cs` - Space descent and landing sequence
- `AutoParkSystem.cs` - Automatic parking at nightclub
- `ArchetypeManager.cs` - Spawns and manages disappointing male archetypes
- `SimpleTrafficSystem.cs` - Basic traffic AI for city environment

### Utility Scripts
- `SceneSetupManager.cs` - Automated scene configuration
- `ArchetypeBehavior.cs` - Individual archetype AI and dialogue

## Development Notes

### Character Personalities
Each character has distinct dialogue patterns and reactions:
- **MINILAMBOBAE**: Mission-focused, increasingly disappointed
- **BECCA**: Analytical, "I told you so" attitude
- **JENNY**: Eternally optimistic, suggests alternatives
- **ARCHIE**: Sarcastic AI, comments on Earth's inadequacies

### Archetype System
The disappointment system tracks failed scans and adjusts character reactions accordingly. Each archetype has specific dialogue and behavior patterns that reflect their stereotypical nature.

### Future Enhancements
- Mini-games for archetype encounters
- Multiple venue locations
- Expanded dialogue system
- Character customization
- Multiplayer support for squad missions

## Troubleshooting

### Common Issues
1. **Vehicles not moving**: Check Rigidbody and WheelCollider setup
2. **AI not following**: Ensure target is assigned to AIFollowerVehicle
3. **No dialogue**: Check UI Text components and AudioSource setup
4. **Cutscene not playing**: Verify OpeningCutscene component and positions

### Performance Tips
- Use object pooling for traffic vehicles
- Limit active archetype count
- Optimize particle effects for mobile
- Use LOD system for distant objects

## Credits
- Vehicle physics based on Unity's WheelCollider system
- Input handling via Unity's new Input System
- Character dialogue system with personality-driven responses
- Procedural archetype spawning with disappointment tracking

For support and updates, visit the HOT PPL development repository.
