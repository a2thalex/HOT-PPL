# Unity Compilation Troubleshooting Guide
## HOT PPL - FIRST CONTACT

### Quick Fix (Most Common Solution)

1. **Close Unity completely**
2. **Run the fix script**: `FixUnityCompilation.bat` or `FixUnityCompilation.ps1`
3. **Reopen project in Unity**
4. **Wait for reimport and compilation**

### Common Errors and Solutions

#### Error: `Mono.Cecil.AssemblyResolutionException`
**Cause**: Assembly dependency conflicts or missing references
**Solution**: 
- Run the compilation fix script
- Clear Library folder
- Update package manifest

#### Error: `CS8803: Top-level statements must precede namespace`
**Cause**: Code outside class definitions
**Solution**: 
- Check all .cs files for code outside classes
- Move any loose code into appropriate methods

#### Error: `The type or namespace name 'InputSystem' could not be found`
**Cause**: Missing Input System package
**Solution**: 
- Verify Input System package in Package Manager
- Check assembly definition references

#### Error: `Assembly 'Assembly-CSharp-Editor' not found`
**Cause**: Editor assembly compilation issues
**Solution**: 
- Delete Library folder
- Reimport all assets
- Check for Editor-only scripts in runtime folders

### Manual Fix Steps

If the automated scripts don't work:

#### 1. Package Manifest Fix
Edit `Packages/manifest.json`:
```json
{
  "dependencies": {
    "com.unity.inputsystem": "1.8.2",
    "com.unity.textmeshpro": "3.2.0-pre.4",
    "com.unity.ugui": "2.0.0",
    "com.unity.modules.accessibility": "1.0.0",
    "com.unity.modules.ai": "1.0.0",
    "com.unity.modules.animation": "1.0.0",
    "com.unity.modules.audio": "1.0.0",
    "com.unity.modules.physics": "1.0.0",
    "com.unity.modules.ui": "1.0.0",
    "com.unity.modules.vehicles": "1.0.0"
  }
}
```

#### 2. Assembly Definition Fix
Create `Assets/Scripts/HOTPPLRuntime.asmdef`:
```json
{
    "name": "HOTPPLRuntime",
    "references": [
        "Unity.InputSystem",
        "Unity.TextMeshPro",
        "UnityEngine.UI"
    ],
    "autoReferenced": true
}
```

#### 3. Script Organization
Ensure proper folder structure:
```
Assets/
├── Scripts/
│   ├── HOTPPLRuntime.asmdef
│   ├── VehicleController.cs
│   ├── ArchiePersonality.cs
│   └── [other runtime scripts]
├── Editor/
│   └── [editor-only scripts]
└── Input/
    └── VehicleInputActions.inputactions
```

### Unity Version Compatibility

#### Recommended Versions
- **Unity 6.2.0f1** (stable release)
- **Unity 2023.3 LTS** (most stable)

#### Avoid These Versions
- Unity 6.0 Beta versions
- Unity 6.1 Alpha versions
- Any version with AI packages in beta

### Package Compatibility Issues

#### Problematic Packages (Remove if present)
```json
"com.unity.ai.assistant": "1.0.0-pre.7",
"com.unity.ai.generators": "1.0.0-pre.14", 
"com.unity.ai.inference": "2.2.1",
"com.justinpbarnett.unity-mcp": "..."
```

#### Essential Packages (Keep these)
```json
"com.unity.inputsystem": "1.8.2",
"com.unity.textmeshpro": "3.2.0-pre.4",
"com.unity.ugui": "2.0.0"
```

### Advanced Troubleshooting

#### Clear All Unity Cache
```bash
# Windows
rmdir /s /q "%APPDATA%\Unity\Asset Store-5.x"
rmdir /s /q "%LOCALAPPDATA%\Unity\cache"

# macOS
rm -rf ~/Library/Unity/Asset\ Store-5.x
rm -rf ~/Library/Unity/cache
```

#### Reset Unity Preferences
```bash
# Windows Registry
reg delete "HKEY_CURRENT_USER\Software\Unity Technologies" /f

# macOS
defaults delete com.unity3d.UnityEditor5.x
```

#### Force Package Refresh
1. Delete `Packages/packages-lock.json`
2. Delete `Library/PackageCache`
3. Reopen Unity

### Script-Specific Issues

#### ArchiePersonality.cs Issues
- Ensure all methods are inside the class
- Check for missing using statements
- Verify enum definitions are outside class

#### Input System Issues
- Verify `.inputactions` file is properly configured
- Check PlayerInput component references
- Ensure Input System package is installed

#### UI System Issues
- Verify TextMeshPro package is installed
- Check UI package references
- Ensure Canvas components are properly set up

### Performance Optimization

#### Reduce Compilation Time
1. Use assembly definition files
2. Minimize script dependencies
3. Avoid circular references
4. Use precompiled assemblies for third-party code

#### Memory Usage
1. Clear Library folder regularly during development
2. Use Unity's Package Manager to remove unused packages
3. Optimize script compilation order

### Emergency Recovery

#### If Project Won't Open
1. Create new Unity project
2. Copy `Assets` folder from broken project
3. Manually recreate `ProjectSettings`
4. Import scripts one by one to identify issues

#### If Scripts Won't Compile
1. Comment out all custom scripts
2. Fix compilation errors one script at a time
3. Use Unity's built-in script templates
4. Check for Unity API changes

### Getting Help

#### Unity Console Messages
- Always check Console window first
- Look for the first error (others may be cascading)
- Use Console filters to focus on errors

#### Unity Editor Log
**Windows**: `%LOCALAPPDATA%\Unity\Editor\Editor.log`
**macOS**: `~/Library/Logs/Unity/Editor.log`

#### Community Resources
- Unity Forums
- Unity Discord
- Stack Overflow (unity3d tag)
- Unity Documentation

### Prevention Tips

1. **Use stable Unity versions** for production
2. **Backup projects** before major changes
3. **Test package updates** in separate projects
4. **Use version control** (Git) for all projects
5. **Document custom modifications** for future reference

### Success Indicators

After applying fixes, you should see:
- ✅ No compilation errors in Console
- ✅ All scripts show as compiled
- ✅ Input System working
- ✅ UI elements displaying correctly
- ✅ ARCHIE humor system functional

If you still have issues after following this guide, the problem may be environment-specific and require individual troubleshooting.
