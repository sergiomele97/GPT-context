using Microsoft.Win32;
using System;
using System.IO;
using System.Reflection;

namespace ContextInstaller
{
    internal class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Listar recursos incorporados
                ListEmbeddedResources();

                // Ruta del directorio de instalación
                string installDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "GPT-context");
                Console.WriteLine($"Directorio de instalación: {installDir}");

                // Verificar el directorio de instalación
                if (!Directory.Exists(installDir))
                {
                    Console.WriteLine("Creando directorio de instalación...");
                    Directory.CreateDirectory(installDir);
                }

                // Mover el ejecutable
                string exeName = "context.exe"; // Nombre del ejecutable
                string destExePath = Path.Combine(installDir, exeName); // Nombre destino

                if (File.Exists("../../../context.exe")) // Instalación desde el repositorio (Development)
                {
                    // Verifica si el archivo ya existe en el destino y lo elimina si es necesario
                    if (File.Exists(destExePath))
                    {
                        File.Delete(destExePath); // Elimina el archivo en destino si ya existe
                    }

                    // Mover el ejecutable desde la ubicación del repositorio a la ruta de instalación
                    File.Copy("../../../context.exe", destExePath);
                }
                else // Instalación desde zip
                {
                    // Extraer el archivo .exe desde los recursos
                    string resourceName = "ContextInstaller.context.exe";
                    ExtractResource(resourceName, destExePath);
                }

                Console.WriteLine("Moviendo el ejecutable...");
                Console.WriteLine($"Ejecutable extraído a: {destExePath}");

                // Extraer el icono a la carpeta de instalación
                string iconPath = Path.Combine(installDir, "icon.ico");
                ExtractIcon(iconPath);

                // Añadir al PATH
                Console.WriteLine("Añadiendo al PATH...");
                AddToPath(installDir);

                // Editar registro windows (click derecho sobre archivos y carpetas)
                RegistroMenu.CrearMenuCascada();

                // Mensaje de finalización
                Console.WriteLine("\nInstalación completada con éxito!\n");
                Console.WriteLine("\nPresiona cualquier tecla para salir...");
                Console.ReadKey();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }

        static void ExtractResource(string resourceName, string outputPath)
        {
            using (Stream stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(resourceName))
            {
                if (stream == null)
                {
                    throw new FileNotFoundException($"No se encontró el recurso: {resourceName}");
                }

                using (FileStream fileStream = new FileStream(outputPath, FileMode.Create, FileAccess.Write))
                {
                    stream.CopyTo(fileStream);
                }
            }
        }

        static void ListEmbeddedResources()
        {
            var resourceNames = Assembly.GetExecutingAssembly().GetManifestResourceNames();
            Console.WriteLine("Recursos incrustados:");
            foreach (var resourceName in resourceNames)
            {
                Console.WriteLine(resourceName);
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

        static void ExtractIcon(string iconPath)
        {
            string resourceName = "ContextInstaller.icon.ico"; // Nombre completo del recurso
            using (Stream stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(resourceName))
            {
                if (stream == null)
                {
                    throw new FileNotFoundException($"No se encontró el recurso: {resourceName}");
                }

                using (FileStream fileStream = new FileStream(iconPath, FileMode.Create, FileAccess.Write))
                {
                    stream.CopyTo(fileStream);
                }
            }
            Console.WriteLine($"Icono extraído a: {iconPath}");
        }
    }
}
