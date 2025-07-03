# HOT PPL: The Search - Vehicle System

This directory contains the complete vehicle system for the Lamborghini in HOT PPL: The Search, featuring realistic physics, seamless character integration, and professional camera behavior.

## System Overview

The vehicle system is built using Unity's WheelCollider system and follows the specifications from the development plan:

- **Realistic Lamborghini Physics** with high-performance sports car characteristics
- **Seamless Character Integration** with smooth entry/exit transitions
- **Professional Camera System** with multiple view modes
- **Comprehensive Audio System** with engine, tire, and wind sounds
- **Modular Design** ready for customization and multiplayer integration

## Core Components

### VehicleController.cs
The main vehicle physics controller featuring:

- **WheelCollider Physics**: Realistic tire simulation with proper friction curves
- **Lamborghini Characteristics**: RWD, high-performance tuning, sports car handling
- **Power Delivery**: Realistic acceleration curve with speed-based torque reduction
- **Advanced Features**: Downforce, speed-sensitive steering, handbrake drifting
- **Input Integration**: New Input System with vehicle action map

**Key Features:**
- Rear-wheel drive (RWD) configuration
- Realistic suspension and tire physics
- Speed-sensitive steering response
- Handbrake with drift capability
- Downforce for high-speed stability
- Performance monitoring integration

### LamborghiniSettings.cs
ScriptableObject for vehicle tuning:

- **Complete Physics Tuning**: Mass, drag, suspension, tire friction
- **Engine Performance**: Torque curves, RPM ranges, power delivery
- **Handling Characteristics**: Steering response, brake balance
- **Audio Settings**: Engine pitch curves, volume settings
- **Visual Effects**: Exhaust intensity, tire smoke thresholds

**Tuning Categories:**
- Vehicle Physics (mass, drag, downforce)
- Engine Performance (torque, speed, RPM)
- Braking System (brake torque, handbrake)
- Steering (angle limits, speed sensitivity)
- Suspension (spring rates, damping)
- Tire Friction (forward/sideways curves)

### VehicleEntry.cs
Seamless character-to-vehicle transitions:

- **IInteractable Integration**: Works with character interaction system
- **Smooth Transitions**: Animated entry/exit sequences
- **Input Map Switching**: Automatic Player ↔ Vehicle input switching
- **Camera Transitions**: Smooth character ↔ vehicle camera switching
- **Player Visibility**: Hide player when inside vehicle

**Entry/Exit Features:**
- Multiple entry points (driver/passenger sides)
- Range-based interaction detection
- Smooth position interpolation
- Component state management
- Visual feedback and prompts

### VehicleCameraController.cs
Professional driving camera system:

- **Multiple Camera Modes**: Third-person, first-person, hood, cinematic
- **Cinemachine Integration**: Professional camera behavior
- **Speed-Responsive**: Dynamic camera positioning based on velocity
- **Smooth Transitions**: Seamless mode switching
- **Look-Ahead System**: Predictive camera positioning

**Camera Modes:**
- Third-Person: Dynamic follow camera with speed offset
- First-Person: Driver's eye view with free look
- Hood: Stable hood-mounted camera
- Cinematic: Dramatic angles for replays

### VehicleAudio.cs
Comprehensive audio system:

- **Engine Audio**: RPM-based pitch and volume with realistic curves
- **Tire Audio**: Speed and slip-based tire squeal
- **Wind Audio**: Speed-based wind noise
- **Transmission Audio**: Gear shift sounds and engine start/stop
- **3D Spatial Audio**: Proper positioning and rolloff

**Audio Features:**
- Dynamic engine pitch based on RPM
- Tire squeal during drifting
- Wind noise at high speeds
- Gear shift sound effects
- Engine start/stop sequences

### VehicleSetup.cs
Automated vehicle creation:

- **Complete Vehicle Generation**: Creates all components automatically
- **Wheel System Setup**: Proper WheelCollider and mesh configuration
- **Component Integration**: Automatically wires all vehicle systems
- **Visual Creation**: Basic Lamborghini-style body and wheels
- **Testing Tools**: Fleet creation for testing scenarios

## Integration with Game Systems

### Character System Integration
- **Seamless Transitions**: Smooth character-to-vehicle entry/exit
- **Input System Coordination**: Automatic action map switching
- **Camera Coordination**: Smooth camera transitions
- **Interaction Framework**: Uses existing IInteractable system

### Social System Integration
- **Vehicle Customization**: Color and style changes affect social status
- **Driving Skill**: Performance affects social evaluation
- **Multiplayer Ready**: Passenger system for social interactions
- **Status Symbol**: Lamborghini ownership impacts relationships

### Performance Integration
- **MCP Monitoring**: Real-time performance tracking during driving
- **60 FPS Target**: Optimized for smooth gameplay
- **Efficient Physics**: Minimal performance impact
- **LOD Ready**: Prepared for distance-based optimization

## Vehicle Specifications

### Lamborghini Performance Profile
Based on real Lamborghini Huracán specifications:

- **Mass**: 1500kg (realistic sports car weight)
- **Power**: High torque with realistic power curve
- **Top Speed**: ~360 km/h (100 m/s in Unity)
- **Acceleration**: 0-100 km/h in ~3 seconds
- **Handling**: Rear-wheel drive with excellent grip
- **Braking**: High-performance brake system

### Physics Tuning
- **Suspension**: Sports car setup with low ride height
- **Tires**: High-performance with good grip and drift capability
- **Aerodynamics**: Downforce for high-speed stability
- **Center of Mass**: Low and rear-biased for sports car handling

## Usage Instructions

### Creating a Vehicle
1. **Automatic Setup**: Use `VehicleSetup.CreateLamborghiniVehicle()`
2. **Manual Setup**: Add components to existing GameObject
3. **Prefab Creation**: Save configured vehicle as prefab
4. **Testing**: Use `TestSceneSetup` to create test environment

### Tuning the Vehicle
1. **Create Settings Asset**: Right-click → Create → HOTPPL → Vehicle → Lamborghini Settings
2. **Adjust Parameters**: Modify physics, engine, and handling settings
3. **Assign to Vehicle**: Drag settings to VehicleController
4. **Test and Iterate**: Use test scene to validate changes

### Character Integration
1. **Ensure Interaction System**: Player must have InteractionSystem component
2. **Position Vehicle**: Place within interaction range of player
3. **Test Entry/Exit**: Verify smooth transitions work correctly
4. **Input Validation**: Confirm action maps switch properly

## Performance Considerations

### Optimization Features
- **Efficient WheelColliders**: Minimal physics overhead
- **LOD Ready**: Prepared for distance-based optimization
- **Audio Optimization**: Spatial audio with proper rolloff
- **Effect Management**: Conditional particle and trail systems

### Performance Targets
- **60 FPS**: Maintains target framerate during driving
- **Low Memory**: Efficient asset usage
- **Smooth Physics**: Stable at high speeds
- **Quick Loading**: Fast instantiation and setup

## Development Workflow

### Adding New Vehicle Types
1. **Create New Settings**: Derive from LamborghiniSettings
2. **Adjust Parameters**: Tune for different vehicle characteristics
3. **Update Audio**: Add vehicle-specific engine sounds
4. **Test Integration**: Verify with character and camera systems

### Customization System
1. **Visual Customization**: Color, materials, decals
2. **Performance Tuning**: Engine upgrades, tire compounds
3. **Audio Customization**: Different engine sounds
4. **Social Integration**: Customization affects social status

### Multiplayer Preparation
1. **Network Components**: Ready for network synchronization
2. **State Management**: Clean separation of local/networked state
3. **Input Handling**: Prepared for remote player input
4. **Passenger System**: Framework for multiple occupants

## Testing and Validation

### Test Scenarios
- **Basic Driving**: Movement, steering, acceleration, braking
- **Entry/Exit**: Character transitions and input switching
- **Camera System**: All camera modes and transitions
- **Audio System**: Engine, tire, and wind audio
- **Performance**: 60 FPS during high-speed driving

### Debug Features
- **Gizmos**: Visual debugging for physics and interaction ranges
- **Console Logging**: Detailed state information
- **Performance Monitoring**: MCP integration for real-time metrics
- **Component Validation**: Automatic setup verification

## Next Steps

### Immediate Enhancements (Phase 2 completion)
1. **Audio Assets**: Real Lamborghini engine sounds
2. **Visual Polish**: Improved vehicle model and materials
3. **Effect Systems**: Exhaust particles, tire smoke, brake lights
4. **UI Integration**: Speedometer, gear indicator, fuel gauge

### Future Features (Later Phases)
1. **Vehicle Customization**: Paint jobs, rims, performance upgrades
2. **Damage System**: Visual and performance damage
3. **Racing Features**: Lap times, racing lines, competition modes
4. **Multiplayer Integration**: Passenger system, synchronized driving

## Validation Checklist

- [x] Vehicle physics feel realistic and responsive
- [x] Character entry/exit transitions work smoothly
- [x] Camera system provides good driving experience
- [x] Audio system enhances immersion
- [x] Input system switches correctly between character/vehicle
- [x] Performance targets met (60 FPS)
- [ ] Real audio assets integrated
- [ ] Visual effects system complete
- [ ] Customization system implemented
- [ ] Multiplayer synchronization ready

This vehicle system provides a solid foundation for the Lamborghini driving experience in HOT PPL: The Search, with realistic physics, professional camera work, and seamless integration with the character system.
