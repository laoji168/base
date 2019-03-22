@ECHO OFF
REM Programming in Go by Mark Summerfield ISBN: 0321774639

REM Execute this batch file in a console before using the Go tools.
REM Or, if you want to be able to use the tools at anytime, set
REM the GOROOT and GOPATH environment variables as described in the
REM book, or create an MS-DOS Prompt/Command Prompt shortcut and
REM tell it to execute this batch file at startup by changing the
REM shortcut's Properties' Target by adding
REM "/k %HOMEPATH%\goeg\gopath.bat" (without the quotes) at the end.

REM Uncomment the two SET commands below if you installed and built from
REM source instead of installing a binary package, and change the GOROOT
REM path if necessary. If you installed a binary package the GOROOT
REM environment variable is already permanently set, and the PATH already
REM includes the Go tools.
REM SET GOROOT=C:\Go
REM SET PATH=%PATH%;%GOROOT%\bin

REM Tell your shell where to find the Go book's examples (HOMEPATH\goeg)
REM and your own code (HOMEPATH\app\go); change the paths if necessary.
REM If you don't need the book's examples anymore just change it to have
REM a single path. Important: wherever you put your own Go programs must
REM have a src directory, e.g., HOMEPATH\app\go\src, with your programs
REM and packages inside it, e.g., HOMEPATH\app\go\src\myapp.
SET GOPATH=%HOMEPATH%\app\go;%HOMEPATH%\goeg

REM Some of the examples output non-ASCII characters to the console
REM using the UTF-8 Unicode encoding. Modern versions of Windows can
REM cope with this by changing the code page to 65001. This can cause
REM problems with older versions of Windows, in which case comment out
REM the following line.
CHCP 65001
