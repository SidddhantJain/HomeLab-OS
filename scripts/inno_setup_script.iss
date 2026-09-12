; Inno Setup Installer Script for HomeLab OS v5.0
#define MyAppName "HomeLab OS"
#define MyAppVersion "5.0.0"
#define MyAppPublisher "HomeLab OS Open Source Team"
#define MyAppURL "https://github.com/SidddhantJain/HomeLab-OS"
#define MyAppExeName "HomeLabOS-Setup-Wizard.exe"

[Setup]
AppId={D8A109F2-5C32-4E18-9127-8B1E9A4B8F3D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\HomeLab OS
DefaultGroupName={#MyAppName}
OutputDir=D:\Siddhant\projects\HomeLab OS\release\installers
OutputBaseFilename=HomeLabOS-Setup-v5.0.0
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "D:\Siddhant\projects\HomeLab OS\start_server.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Siddhant\projects\HomeLab OS\start_manager.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Siddhant\projects\HomeLab OS\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\HomeLab OS Server"; Filename: "{app}\start_server.bat"
Name: "{autoprograms}\HomeLab OS Desktop Manager"; Filename: "{app}\start_manager.bat"
Name: "{autodesktop}\HomeLab OS Desktop Manager"; Filename: "{app}\start_manager.bat"; Tasks: desktopicon

[Run]
Filename: "{app}\start_manager.bat"; Description: "Launch HomeLab OS Desktop Manager Console"; Flags: postinstall nowait shellexec skipifsilent
