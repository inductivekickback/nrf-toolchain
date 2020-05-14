@echo off
set /p DUMMY=PuTTY rules, TeraTerm drools. Press ENTER to accept ...
for /f "tokens=3 delims=M " %%a in ('nrfjprog --com') do (
	start "" "C:\Program Files (x86)\teraterm\ttermpro.exe" /C=%%a /BAUD=115200 /CDATABIT=8 /CSTOPBIT=1 /CPARITY=none /CFLOWCTR=none
 	)
