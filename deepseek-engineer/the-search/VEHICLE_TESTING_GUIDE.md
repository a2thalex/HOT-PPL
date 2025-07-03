# HOT PPL: The Search - Vehicle System Testing Guide

This guide will help you test the complete vehicle system we just implemented, including the character controller, Lamborghini vehicle, and all integration features.

## 🚀 Quick Start Testing

### Step 1: Open Unity Project
1. **Unity should be opening automatically** via Unity Hub
2. If not, open Unity Hub and select the `HOTPPLTheSearch` project
3. Wait for Unity to load and compile all scripts

### Step 2: Create Test Scene
1. **Option A - Use Existing Scene:**
   - Open `Assets/Scenes/VehicleTestScene.unity` (if it loads properly)
   
2. **Option B - Create New Scene:**
   - File → New Scene → 3D (Built-in Render Pipeline)
   - Add an empty GameObject and name it "TestSceneManager"
   - Add the `TestSceneSetup` component to it
   - Make sure all checkboxes are enabled:
     - ✅ Create Test Environment
     - ✅ Create Player Character  
     - ✅ Create Test Interactables
     - ✅ Create Test Vehicle
   - Press Play to auto-generate the test environment

### Step 3: Verify Scene Setup
After pressing Play, you should see:
- ✅ **Green ground plane** (50x50 units)
- ✅ **Minilambobae character** (capsule with PlayerController)
- ✅ **Red Lamborghini** positioned to the right of the player
- ✅ **Yellow interactable spheres** (bobbing up and down)
- ✅ **Directional light** for proper lighting
- ✅ **Random obstacle cubes** scattered around

## 🎮 Testing Controls

### Character Controls (Default State)
- **WASD** - Move character
- **Mouse** - Look around (camera control)
- **Shift** - Run/sprint
- **E** - Interact with objects
- **Space** - Jump (if implemented)

### Vehicle Controls (When in Lamborghini)
- **W** - Accelerate
- **S** - Brake/Reverse
- **A/D** - Steer left/right
- **Shift** - Handbrake (for drifting)
- **F** - Exit vehicle
- **V** - Switch camera modes

## 🧪 Test Scenarios

### Test 1: Character Movement
1. **Basic Movement:**
   - Use WASD to move around
   - Verify smooth movement in all directions
   - Check camera follows properly
   - Test running with Shift

2. **Expected Results:**
   - ✅ Smooth character movement
   - ✅ Camera follows without jitter
   - ✅ Character rotates to face movement direction
   - ✅ Running increases movement speed

### Test 2: Vehicle Entry
1. **Approach Vehicle:**
   - Walk the character toward the red Lamborghini
   - Get within ~3 units of the vehicle
   - Look for interaction prompt: "Press E to enter Lamborghini"

2. **Enter Vehicle:**
   - Press E when prompt appears
   - Watch the entry animation
   - Verify character disappears (inside vehicle)
   - Check camera switches to vehicle mode

3. **Expected Results:**
   - ✅ Interaction prompt appears near vehicle
   - ✅ Smooth entry animation
   - ✅ Character becomes invisible (inside car)
   - ✅ Camera switches to third-person vehicle view
   - ✅ Input switches to vehicle controls

### Test 3: Vehicle Driving
1. **Basic Driving:**
   - Use W to accelerate
   - Use A/D to steer
   - Use S to brake
   - Test at different speeds

2. **Advanced Driving:**
   - Try high-speed driving
   - Test sharp turns
   - Use handbrake (Shift) for drifting
   - Test braking from high speed

3. **Expected Results:**
   - ✅ Realistic acceleration and deceleration
   - ✅ Responsive steering (less sensitive at high speed)
   - ✅ Proper wheel rotation and suspension
   - ✅ Handbrake enables drifting
   - ✅ Vehicle feels like a sports car

### Test 4: Camera System
1. **Camera Modes:**
   - Press V to cycle through camera modes
   - Test: Third-person → First-person → Hood → back to Third-person
   - Drive in each mode to test behavior

2. **Camera Behavior:**
   - Check smooth following in third-person
   - Verify first-person view from driver position
   - Test hood camera stability

3. **Expected Results:**
   - ✅ Smooth transitions between camera modes
   - ✅ Third-person camera follows vehicle dynamically
   - ✅ First-person view from correct driver position
   - ✅ Hood camera provides stable forward view
   - ✅ All cameras respond to vehicle movement

### Test 5: Vehicle Exit
1. **Exit Vehicle:**
   - While driving, press F to exit
   - Watch the exit animation
   - Verify character appears outside vehicle
   - Check camera switches back to character mode

2. **Expected Results:**
   - ✅ Smooth exit animation
   - ✅ Character appears at driver's side
   - ✅ Camera switches back to character view
   - ✅ Input switches back to character controls
   - ✅ Can walk away from vehicle normally

### Test 6: Audio System
1. **Engine Audio:**
   - Listen for engine sound when vehicle starts
   - Rev the engine (W key) and listen for pitch changes
   - Test at different RPMs

2. **Environmental Audio:**
   - Drive fast and listen for wind noise
   - Try drifting to hear tire squeal
   - Test engine start/stop sounds

3. **Expected Results:**
   - ✅ Engine sound starts when entering vehicle
   - ✅ Engine pitch changes with RPM
   - ✅ Wind noise at high speeds
   - ✅ Tire squeal during drifting
   - ✅ 3D spatial audio positioning

## 🐛 Troubleshooting

### Common Issues and Solutions

**Issue: Scripts don't compile**
- Solution: Check Unity Console for errors
- Ensure all using statements are correct
- Verify Unity Input System package is installed

**Issue: Character doesn't move**
- Solution: Check PlayerInput component is assigned
- Verify Input Actions asset is loaded
- Check character has CharacterController component

**Issue: Vehicle doesn't respond**
- Solution: Verify WheelColliders are assigned
- Check vehicle has Rigidbody component
- Ensure vehicle is on ground (not floating)

**Issue: Camera doesn't follow**
- Solution: Check Cinemachine package is installed
- Verify camera targets are assigned
- Check camera priorities are set correctly

**Issue: No audio**
- Solution: Check AudioSource components exist
- Verify audio clips are assigned (may be null in test)
- Check Unity audio settings

**Issue: Vehicle falls through ground**
- Solution: Ensure ground has collider
- Check vehicle colliders are properly set up
- Verify physics layers are correct

**Issue: Entry/exit doesn't work**
- Solution: Check interaction range (get closer)
- Verify VehicleEntry component exists
- Check IInteractable implementation

## 📊 Performance Testing

### Performance Targets
- **Target FPS:** 60 FPS
- **Memory Usage:** Stable (no leaks)
- **Physics:** Smooth at all speeds

### Performance Checks
1. **Open Unity Profiler** (Window → Analysis → Profiler)
2. **Monitor while testing:**
   - CPU usage during driving
   - Memory allocation
   - Physics performance
   - Audio performance

3. **Expected Performance:**
   - ✅ Consistent 60+ FPS
   - ✅ No memory leaks
   - ✅ Smooth physics simulation
   - ✅ No audio dropouts

## 🎯 Success Criteria

### ✅ Complete Success Checklist
- [ ] Character moves smoothly with WASD
- [ ] Camera follows character properly
- [ ] Vehicle entry prompt appears and works
- [ ] Smooth entry animation and input switching
- [ ] Vehicle drives realistically (acceleration, steering, braking)
- [ ] Handbrake enables drifting
- [ ] Camera modes switch with V key
- [ ] Vehicle exit works smoothly
- [ ] Audio system provides engine, tire, and wind sounds
- [ ] Performance maintains 60 FPS
- [ ] No console errors during testing

### 🏆 Advanced Testing
If basic tests pass, try these advanced scenarios:
- **High-speed driving** (test stability)
- **Drift challenges** (handbrake + steering)
- **Multiple entry/exit cycles** (test reliability)
- **Camera mode switching while driving**
- **Interaction with other test objects**

## 📝 Reporting Results

### If Everything Works:
🎉 **Congratulations!** The vehicle system is working perfectly. You now have:
- Complete character controller with third-person movement
- Realistic Lamborghini vehicle with proper physics
- Seamless character-to-vehicle transitions
- Professional camera system with multiple modes
- Immersive audio system
- Performance-optimized implementation

### If Issues Found:
📋 **Report the following:**
1. **What you were testing** (which scenario)
2. **What you expected** (from this guide)
3. **What actually happened** (describe the issue)
4. **Console errors** (if any)
5. **Performance impact** (FPS drops, etc.)

This will help us quickly identify and fix any issues with the vehicle system implementation.

## 🚀 Next Steps After Testing

Once testing is complete and successful:
1. **Save the test scene** for future reference
2. **Create vehicle prefabs** for easy reuse
3. **Tune vehicle settings** using LamborghiniSettings ScriptableObject
4. **Add visual polish** (better models, materials, effects)
5. **Implement social interaction system** (next development phase)

Happy testing! 🚗💨
