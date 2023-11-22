Set objShell = CreateObject("WScript.Shell")
objShell.Run "taskkill /F /IM python.exe"
objShell.Run "taskkill /F /IM node.exe"
Set objShell = Nothing
