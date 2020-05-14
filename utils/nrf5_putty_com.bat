@echo off
for /f "tokens=2" %%a in ('nrfjprog --com') do (
	start "" "putty.exe" -serial %%a -sercfg 115200,8,n,1,N
	)
