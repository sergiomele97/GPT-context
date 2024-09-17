﻿namespace InstallerApp
{
    using System;
    using System.Diagnostics;
    using System.IO;
    using System.Net;

    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Directorio base del repositorio (donde se encuentra el ejecutable del instalador)
                string baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
                Console.WriteLine(baseDirectory);

                // Directorio del entorno virtual
                string venvPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "myenv");

                // Ruta del script Python en relación con el directorio base del repositorio
                string scriptPath = Path.Combine(baseDirectory, "src", "context.py");

                // Ruta del directorio de instalación
                string installDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "GPT-context");
                Console.WriteLine($"Directorio de instalación: {installDir}");

                // Verificar si Python está instalado
                if (!IsPythonInstalled())
                {
                    Console.WriteLine("Python no está instalado. Descargando e instalando Python...");
                    InstallPython();
                }
                else
                {
                    Console.WriteLine("Python ya está instalado.");
                }

                // Crear entorno virtual si no existe
                if (!Directory.Exists(venvPath))
                {
                    Console.WriteLine("Creando entorno virtual...");
                    RunCommand("python", $"-m venv \"{venvPath}\"");
                    Console.WriteLine("Instalando pip...");
                    ActivateAndRunCommand(venvPath, "python -m ensurepip");
                    Console.WriteLine("Instalando PyInstaller...");
                    ActivateAndRunCommand(venvPath, "pip install pyinstaller");
                }
                else
                {
                    Console.WriteLine("El entorno virtual ya existe.");
                }

                // Limpiar archivos temporales de PyInstaller si existen
                string distDir = Path.Combine(baseDirectory, "dist");
                string buildDir = Path.Combine(baseDirectory, "build");
                string specFile = Path.Combine(baseDirectory, "context.spec");

                if (Directory.Exists(distDir))
                {
                    Console.WriteLine("Eliminando directorio dist...");
                    Directory.Delete(distDir, true);
                }

                if (Directory.Exists(buildDir))
                {
                    Console.WriteLine("Eliminando directorio build...");
                    Directory.Delete(buildDir, true);
                }

                if (File.Exists(specFile))
                {
                    Console.WriteLine("Eliminando archivo spec...");
                    File.Delete(specFile);
                }

                Console.WriteLine("Generando ejecutable con PyInstaller...");
                ActivateAndRunCommand(venvPath, $"pyinstaller --onefile \"{scriptPath}\"");

                // Verificar si el archivo ejecutable ha sido creado
                string exePath = Path.Combine(distDir, "context.exe");
                if (!File.Exists(exePath))
                {
                    throw new FileNotFoundException("No se encontró el archivo ejecutable generado por PyInstaller.");
                }

                // Crear directorio de instalación
                if (!Directory.Exists(installDir))
                {
                    Console.WriteLine("Creando directorio de instalación...");
                    Directory.CreateDirectory(installDir);
                }

                Console.WriteLine("Moviendo el ejecutable...");
                // Mover el ejecutable
                string destExePath = Path.Combine(installDir, "context.exe");
                File.Copy(exePath, destExePath, true);

                Console.WriteLine("Añadiendo al PATH...");
                // Añadir al PATH
                AddToPath(installDir);

                // Final bueno
                Console.WriteLine("\nInstalación completada con éxito!\n");
                Exito();
                Console.WriteLine("\nPresiona cualquier tecla para salir...");
                Console.ReadKey();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine($"Stack Trace: {ex.StackTrace}");
            }
        }

        static void RunCommand(string fileName, string arguments)
        {
            Console.WriteLine($"Ejecutando: {fileName} {arguments}");

            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = fileName,
                Arguments = arguments,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(startInfo))
            {
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                Console.WriteLine($"Salida: {output}");
                if (!string.IsNullOrEmpty(error))
                {
                    Console.WriteLine($"Error: {error}");
                    throw new Exception($"Error al ejecutar el comando: {error}");
                }
            }
        }

        static void ActivateAndRunCommand(string venvPath, string arguments)
        {
            Console.WriteLine($"Activando entorno virtual y ejecutando: {arguments}");

            string activateScript = Path.Combine(venvPath, "Scripts", "activate.bat");
            string command = $"/c \"{activateScript} && {arguments}\"";

            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "cmd.exe",
                Arguments = command,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(startInfo))
            {
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                Console.WriteLine($"Salida: {output}");
                if (!string.IsNullOrEmpty(error))
                {
                    Console.WriteLine($"Error: {error}");
                    // throw new Exception($"Error al ejecutar el comando: {error}");
                }

                Console.WriteLine($"Código de salida: {process.ExitCode}");
            }
        }

        static void AddToPath(string folderPath)
        {
            Console.WriteLine($"Añadiendo {folderPath} al PATH");

            string pathEnv = Environment.GetEnvironmentVariable("PATH", EnvironmentVariableTarget.User);
            if (!pathEnv.Contains(folderPath))
            {
                Environment.SetEnvironmentVariable("PATH", $"{pathEnv};{folderPath}", EnvironmentVariableTarget.User);
                Console.WriteLine($"Directorio añadido al PATH: {folderPath}");
            }
            else
            {
                Console.WriteLine($"El directorio ya está en el PATH: {folderPath}");
            }
        }

        static bool IsPythonInstalled()
        {
            try
            {
                // Ejecutar un comando simple de Python para verificar si está instalado
                RunCommand("python", "--version");
                return true;
            }
            catch
            {
                return false;
            }
        }

        static void InstallPython()
        {
            string pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe"; // URL de la versión de Python que deseas instalar
            string installerPath = Path.Combine(Path.GetTempPath(), "python_installer.exe");

            Console.WriteLine("Descargando el instalador de Python...");
            using (WebClient client = new WebClient())
            {
                client.DownloadFile(pythonInstallerUrl, installerPath);
            }

            Console.WriteLine("Instalando Python...");
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = installerPath,
                Arguments = "/quiet InstallAllUsers=1 PrependPath=1",
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(startInfo))
            {
                process.WaitForExit();
                if (process.ExitCode != 0)
                {
                    throw new Exception("Error al instalar Python.");
                }
            }

            Console.WriteLine("Python instalado correctamente.");
        }

        static void Exito()
        {
            Console.WriteLine("_________________________________¶¶¶¶");
            Console.WriteLine("________________________¶¶¶¶____¶¶¶¶11¶");
            Console.WriteLine("________________________¶¶1¶¶_¶¶¶¶1111¶");
            Console.WriteLine("_______________________¶¶111¶¶¶1111111¶");
            Console.WriteLine("___________________¶¶¶_¶1111¶¶1111111¶");
            Console.WriteLine("___________________¶11¶¶111¶¶111111¶¶");
            Console.WriteLine("___________________¶11¶1111¶111111¶¶");
            Console.WriteLine("__________________¶¶11¶111¶111111¶¶");
            Console.WriteLine("__________________¶11¶111¶¶111111¶");
            Console.WriteLine("__________________¶11¶111¶1111111¶");
            Console.WriteLine("_________________¶11¶111¶11111111¶");
            Console.WriteLine("_________________¶1¶111¶¶1111111¶¶");
            Console.WriteLine("________________¶1¶¶111¶1111111¶¶");
            Console.WriteLine("_______________¶¶1¶111¶1111111¶¶");
            Console.WriteLine("_______________¶¶¶111¶11111111¶");
            Console.WriteLine("______________¶¶¶11¶¶111111111¶");
            Console.WriteLine("______________¶¶11¶¶111111¶¶¶1¶¶");
            Console.WriteLine("_____________¶11¶¶1111111¶111111¶¶");
            Console.WriteLine("___________¶¶¶¶¶1111111¶¶11111111¶¶¶");
            Console.WriteLine("__________¶¶¶1111111¶¶1111111111111¶¶¶");
            Console.WriteLine("_________¶¶111111¶¶¶11111111111111111¶¶¶¶");
            Console.WriteLine("_________¶111111¶¶1111111111111111111111¶¶¶");
            Console.WriteLine("_________¶111111¶1111111111¶¶¶1111111111111¶");
            Console.WriteLine("________¶11111111111111111¶¶_¶¶¶¶¶¶¶¶111111¶");
            Console.WriteLine("_______¶¶111111111111111¶¶¶________¶111111¶¶");
            Console.WriteLine("_______¶11111111111¶¶¶¶¶¶__________¶111111¶");
            Console.WriteLine("______¶¶11111111111¶¶_____________¶¶11111¶¶");
            Console.WriteLine("______¶111111111111¶______________¶¶11111¶");
            Console.WriteLine("_____¶¶111111111111¶________________¶¶¶¶¶¶¶¶¶¶¶¶");
            Console.WriteLine("_____¶1111111111111¶________________¶¶¶111111¶¶¶¶");
            Console.WriteLine("_____¶1111111111111¶¶_____________¶¶¶111111¶¶¶11¶");
            Console.WriteLine("____¶¶1111111111111¶¶¶_________¶¶¶1111111¶¶11111¶");
            Console.WriteLine("____¶1111111111111111¶¶¶¶¶¶¶¶¶¶¶111111111¶1111¶¶");
            Console.WriteLine("____¶111111111111111111¶¶¶¶11111111111111¶¶¶¶¶¶");
            Console.WriteLine("___¶111111111111111111111111111111111111111¶¶¶");
            Console.WriteLine("__¶111111111111111111111111111111111111111¶¶");
            Console.WriteLine("¶¶11111111111111111111111111111111111111¶¶¶");
            Console.WriteLine("111111111111111111111111111111111¶¶¶¶¶¶¶¶");
            Console.WriteLine("111111111111111111111111111111¶¶¶¶");
            Console.WriteLine("1111111111111111111111111111¶¶¶");
            Console.WriteLine("111111111111111111111111111¶¶");
            Console.WriteLine("1111111111111111111111111¶¶");
            Console.WriteLine("111111111111111111111111¶¶");
            Console.WriteLine("1111111111111111111111¶¶");
            Console.WriteLine("111111111111111111111¶¶");
            Console.WriteLine("1111111111111111111¶¶");
            Console.WriteLine("111111111111111111¶¶");
            Console.WriteLine("1111111111111111¶¶");
            Console.WriteLine("11111111111111¶¶");
            Console.WriteLine("111111111111¶¶");
            Console.WriteLine("1111111111¶¶");
            Console.WriteLine("11111111¶¶");
            Console.WriteLine("111111¶¶");
            Console.WriteLine("1111¶¶");
            Console.WriteLine("11¶¶");
            Console.WriteLine("¶¶");
        }
    }
}

