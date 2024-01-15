Set objShell = CreateObject("WScript.Shell")
objShell.CurrentDirectory = "CamerasMicroservice"
objShell.Run "python runner.py", 0
objShell.CurrentDirectory = "..\ManagementBackend"
objShell.Run "python runner.py", 0
objShell.CurrentDirectory = "..\UserBackend"
objShell.Run "python AppUserBackend.py", 0
objShell.CurrentDirectory = "..\UserFrontend\sport-spot-project"
objShell.Run "npm run serve", 0
Set objShell = Nothing