::network command tool
::btw typing out comments in bash script is so ugly so bare with me if anyone ever reads this

@echo off
title Network Statistics
echo Loading Network Information...
:loop
for /f "tokens=2 delims=:" %%a in ('netsh wlan show interface ^| find "SSID" ^| findstr /v "BSSID"') do set ssid=%%a
:: ^^ essentialy indexes based on the specific command with pipes to find the SSID while excluding the BSSID
:: repeat to pull different specific values from the command
for /f "tokens=2 delims=:" %%a in ('netsh wlan show interface ^| find "Description"') do set adapter=%%a
for /f "tokens=2 delims=:" %%a in ('netsh wlan show interface ^| find "State"') do set state=%%a 
for /f "tokens=2 delims=:" %%a in ('netsh wlan show interface ^| find "Signal"') do set signal=%%a
ping -n 3 8.8.8.8>%temp%\ping.txt
for /f "tokens=4 delims==" %%a in ('type %temp%\ping.txt ^| find "Average"') do set ping=%%a      & ::tokens for ping command changes based on index
for /f "tokens=10 delims= " %%a in ('type %temp%\ping.txt ^| find "Lost"') do set ploss=%%a

cls                             & ::clears
echo Network:
echo --------
echo  SSID:%ssid%
echo  NIC:%adapter%              
echo  STATE:%state%
echo  SIGNAL:%signal%
echo.
echo Speed:
echo -------
echo %ping%
echo  Packet Loss:%ploss%

goto loop


