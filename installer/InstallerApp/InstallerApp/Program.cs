namespace InstallerApp
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

                // Construir la ruta hacia seis directorios atrás usando ../
                string relativePath = @"..\..\..\..\..\..\";
                string targetDirectory = Path.GetFullPath(Path.Combine(baseDirectory, relativePath));

                // Directorio del entorno virtual
                string venvPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "myenv");

                // Ruta del script Python en relación con el directorio base del repositorio
                string scriptPath = Path.Combine(targetDirectory, "src", "context.py");

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

                // Verificar y añadir Python al PATH si no está presente
                AddPythonToPath();

                // Crear entorno virtual si no existe
                if (!Directory.Exists(venvPath))
                {
                    Console.WriteLine("Creando entorno virtual...");
                    RunCommand("python", $"-m venv \"{venvPath}\"");
                    Console.WriteLine("Instalando pip...");
                    ActivateAndRunCommand(venvPath, "python -m ensurepip");
                    Console.WriteLine("Instalando PyInstaller...");
                    ActivateAndRunCommand(venvPath, "pip install pyinstaller");
                    ActivateAndRunCommand(venvPath, "pip install google-generativeai");
                    ActivateAndRunCommand(venvPath, "pip install cryptography");
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
                ActivateAndRunCommand(venvPath, $"pyinstaller --onefile --hidden-import=google.generativeai {scriptPath}");

                // Verificar si el archivo ejecutable ha sido creado
                string exePath = Path.Combine(distDir, "context.exe");
                if (!File.Exists(exePath))
                {
                    throw new FileNotFoundException("No se encontró el archivo ejecutable generado por PyInstaller.");
                }

                // Mueve el archivo a la nueva carpeta
                Console.WriteLine("Moviendo ejecutable a la carpeta del instalador...");

                string destinoDir = "../../../../ContextInstaller";
                try
                {
                    // Asegúrate de que la carpeta de destino existe
                    if (!Directory.Exists(destinoDir))
                    {
                        Directory.CreateDirectory(destinoDir);
                    }

                    // Ruta completa del nuevo archivo
                    string nuevoExePath = Path.Combine(destinoDir, "context.exe");

                    // Elimina el archivo existente si existe
                    if (File.Exists(nuevoExePath))
                    {
                        File.Delete(nuevoExePath);
                    }

                    // Mueve el archivo
                    File.Move(exePath, nuevoExePath);
                    Console.WriteLine("El archivo se ha movido correctamente a " + nuevoExePath);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Se produjo un error al mover el archivo: " + ex.Message);
                }


                Console.WriteLine("\nCompilación completada con éxito!\n");
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
            Console.WriteLine("Esto puede llevar 1-2 minutos");

            string activateScript = Path.Combine(venvPath, "Scripts", "activate.bat");
            if (!File.Exists(activateScript))
            {
                throw new FileNotFoundException("El script de activación del entorno virtual no se encontró.", activateScript);
            }

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

            try
            {
                using (Process process = Process.Start(startInfo))
                {
                    if (process == null)
                    {
                        throw new Exception("No se pudo iniciar el proceso.");
                    }

                    // Captura de errores
                    Task errorTask = Task.Run(() =>
                    {
                        string error;
                        while ((error = process.StandardError.ReadLine()) != null)
                        {
                            // Mostrar errores críticos solo
                            if (error.Contains("ERROR") || error.Contains("Exception") || error.Contains("failed"))
                            {
                                Console.WriteLine($"Error: {error}");
                            }
                        }
                    });

                    // Captura de salida (solo se imprime el mensaje final)
                    Task outputTask = Task.Run(() =>
                    {
                        string output;
                        while ((output = process.StandardOutput.ReadLine()) != null)
                        {
                            // Opcional: Puedes comentar esta línea si no quieres mostrar la salida
                            // Si es necesario, puedes agregar lógica aquí para filtrar la salida
                        }
                    });

                    process.WaitForExit();
                    errorTask.Wait();
                    outputTask.Wait();

                    if (process.ExitCode != 0)
                    {
                        Console.WriteLine($"El comando terminó con código de salida: {process.ExitCode}");
                    }
                    else
                    {
                        Console.WriteLine("El comando se completó con éxito.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al ejecutar el comando: {ex.Message}");
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

        static void AddPythonToPath()
        {
            string pythonPath = GetPythonInstallPath();

            if (pythonPath != null)
            {
                AddToPath(pythonPath);
                Console.WriteLine("Python añadido al PATH.");
            }
            else
            {
                Console.WriteLine("Python ya está añadido al PATH");
            }
        }

        static string GetPythonInstallPath()
        {
            // Intenta encontrar la ruta de instalación de Python
            string[] possiblePaths =
            {
                @"C:\Python39", // Cambia esto a la versión y ruta de Python que estás instalando
                @"C:\Program Files\Python39",
                @"C:\Program Files (x86)\Python39",
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Python39")
            };

            foreach (var path in possiblePaths)
            {
                if (Directory.Exists(path))
                {
                    return path;
                }
            }

            return null;
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

    }
}

