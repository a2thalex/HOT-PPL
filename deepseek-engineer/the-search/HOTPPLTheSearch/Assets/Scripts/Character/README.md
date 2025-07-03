# HOT PPL: The Search - Character System

This directory contains the core character controller system for Minilambobae and other characters in HOT PPL: The Search.

## System Overview

The character system is built using Unity's modern systems and follows the specifications from the development plan:

- **Third-person character controller** with smooth movement
- **Unity's new Input System** for cross-platform input handling
- **Cinemachine camera system** for professional camera behavior
- **Modular interaction system** for NPCs, objects, and vehicles
- **Animation state machine** support for character animations

## Core Components

### PlayerController.cs
The main character controller for Minilambobae featuring:

- **Movement System**: WASD/gamepad movement with camera-relative direction
- **Physics Integration**: Uses CharacterController for reliable collision
- **Speed Control**: Walk/run states with smooth transitions
- **Ground Detection**: Proper ground checking and gravity handling
- **Input Handling**: New Input System integration with action callbacks

**Key Features:**
- Smooth acceleration/deceleration
- Camera-relative movement direction
- Automatic character rotation to face movement
- Interaction system integration
- Movement enable/disable for cutscenes and vehicles

### CharacterAnimator.cs
Handles animation state management:

- **Animation Parameters**: Speed, Grounded, MotionSpeed, Interacting, Talking
- **State Management**: Conversation, emote, and interaction animations
- **Performance Optimized**: Cached parameter IDs for efficiency
- **Modular Design**: Easy to extend for new animation states
- **Root Motion Support**: Optional root motion integration

**Animation States:**
- Idle, Walking, Running (movement)
- Talking (conversations)
- Interacting (object interactions)
- Emotes (social expressions)

### InteractionSystem.cs
Manages player interactions with the world:

- **Range-based Detection**: Configurable interaction range
- **UI Integration**: Automatic interaction prompts
- **Priority System**: Closest object in front of player
- **Interface-based**: Uses IInteractable for extensibility
- **Visual Feedback**: Gizmos for debugging interaction ranges

**Interaction Types:**
- NPCs (conversations, social evaluation)
- Objects (items, doors, switches)
- Vehicles (entry/exit system)
- Environmental elements

### CameraController.cs
Third-person camera system using Cinemachine:

- **Cinemachine Integration**: Professional camera behavior
- **Mouse/Gamepad Support**: Configurable sensitivity settings
- **Smooth Following**: Damped camera movement
- **Angle Constraints**: Vertical angle limits for better control
- **Cursor Management**: Automatic cursor lock/unlock

**Camera Features:**
- Smooth follow and look-at behavior
- Configurable distance and height
- Rotation constraints
- Easy transition system for cutscenes
- Debug visualization

## Input System

### PlayerInputActions.inputactions
Comprehensive input mapping for:

**Player Actions:**
- Move (WASD/Left Stick)
- Look (Mouse/Right Stick)
- Run (Shift/Left Shoulder)
- Interact (E/South Button)
- Jump (Space/East Button)

**Vehicle Actions:**
- Accelerate (W/Right Trigger)
- Brake (S/Left Trigger)
- Steer (AD/Left Stick X)
- Exit Vehicle (F/North Button)

**Control Schemes:**
- Keyboard & Mouse
- Gamepad (Xbox/PlayStation)

## Testing and Setup

### TestSceneSetup.cs
Automated scene setup for testing:

- **Environment Creation**: Ground plane, obstacles, lighting
- **Player Character**: Automatic player setup with all components
- **Test Interactables**: Sample objects for interaction testing
- **Visual Debugging**: Color-coded objects and materials

**Usage:**
1. Add TestSceneSetup to an empty GameObject
2. Run the scene or use context menu "Setup Test Scene"
3. Test character movement, camera, and interactions

## Integration with Game Systems

### Social System Integration
- Character animations for conversations
- Emote system for social expressions
- Interaction prompts for NPCs
- Relationship-based behavior modifications

### Vehicle System Integration
- Movement disable/enable for vehicle entry/exit
- Camera transitions between character and vehicle modes
- Input system switching between action maps
- Position synchronization for seamless transitions

### Multiplayer Integration
- Network-ready component structure
- State synchronization points identified
- Input handling compatible with network players
- Animation parameter networking support

## Performance Considerations

### Optimization Features
- **Cached Animation IDs**: No string lookups during runtime
- **Efficient Ground Checking**: Single sphere cast per frame
- **Conditional Updates**: Systems only update when needed
- **Component Pooling Ready**: Designed for object pooling

### Performance Targets
- 60 FPS on target hardware (GTX 1060/equivalent)
- Minimal garbage collection
- Efficient physics queries
- Smooth animation transitions

## Development Workflow

### Adding New Interactions
1. Implement IInteractable interface
2. Add interaction logic in Interact() method
3. Define interaction prompt text
4. Set up interaction conditions in CanInteract()

### Extending Animations
1. Add new animation parameters to CharacterAnimator
2. Cache parameter IDs in CacheAnimationParameters()
3. Update animation logic in Update methods
4. Add public methods for external control

### Customizing Movement
1. Modify movement parameters in PlayerController
2. Adjust physics settings for different feel
3. Add new movement states as needed
4. Integrate with game-specific mechanics

## MCP Integration

The character system integrates with our MCP servers:

- **Performance Monitoring**: FPS and memory tracking during character movement
- **Git Integration**: Automatic commits when character system milestones are reached
- **Task Management**: Progress tracking for character system development
- **Unity Integration**: Build testing and validation automation

## Next Steps

### Immediate Tasks (Phase 2 completion)
1. **Animation Controller Setup**: Create Animator Controller with proper state machine
2. **Character Model Integration**: Replace capsule with actual character model
3. **Audio Integration**: Footstep sounds and voice clips
4. **Input Polish**: Fine-tune sensitivity and response curves

### Future Enhancements (Later Phases)
1. **Vehicle Integration**: Seamless character-to-vehicle transitions
2. **Social Animations**: Conversation gestures and expressions
3. **Customization System**: Outfit and appearance changes
4. **Multiplayer Sync**: Network character state synchronization

## Validation Checklist

- [x] Character moves smoothly in all directions
- [x] Camera follows without jitter
- [x] Input system responds to keyboard and gamepad
- [x] Interaction system detects nearby objects
- [x] Animation parameters update correctly
- [ ] Animation controller with proper state machine
- [ ] Character model integration
- [ ] Audio system integration
- [ ] Performance targets met (60 FPS)

This character system provides a solid foundation for the HOT PPL: The Search gameplay experience, focusing on smooth movement, reliable interactions, and professional camera behavior.
