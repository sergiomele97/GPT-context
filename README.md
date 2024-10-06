# Instal lattest officially released version:
   ```cmd
   @echo off
   :: Descargar el archivo .rar
   curl -L -o lattest-context-release.rar https://github.com/sergiomele97/GPT-context/releases/download/windows/lattest-context-release.rar

   :: Extraer y ejecutar ContextInstaller.exe (asegúrate de que WinRAR o 7-Zip esté instalado)
   "c:\Program Files\WinRAR\WinRAR.exe" x -o+ "lattest-context-release.rar" && start "" "ContextInstaller.exe"
   ```
# Install lattest changes:

   ```cmd
   git clone https://github.com/sergiomele97/GPT-context.git

   cd GPT-context

   2-install-app.bat
   ```
# If you want to modify the source code, generate an executable and try it on your computer:

   run: 1-compile-app.bat
   then: 2-install-app.bat


   **Note:** If you don't have python, you might need to run 1-compile-app.bat a second time.
   **Note:** If you don't have Git, you can either install it or download the ZIP from the green button on GitHub, unzip it, and run 1-compile-app.bat as an administrator.
