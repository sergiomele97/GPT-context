namespace InstallerApp
{
    using System;
    using System.Diagnostics;
    using System.IO;

    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Directorio base del repositorio (donde se encuentra el ejecutable del instalador)
                string baseDirectory = AppDomain.CurrentDomain.BaseDirectory;

                // Directorio del entorno virtual
                string venvPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "myenv");

                // Ruta del script Python en relación con el directorio base del repositorio
                string scriptPath = Path.Combine(baseDirectory, "src", "context.py");

                // Ruta del directorio de instalación
                string installDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "GPT-context");
                Console.WriteLine($"Directorio de instalación: {installDir}");

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

                Console.WriteLine("\nInstalación completada con exito!\n");
                Exito();
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
