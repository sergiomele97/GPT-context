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

                // Extraer el archivo .exe desde los recursos
                string exeName = "context.exe"; // Aquí solo ponemos el nombre que queremos usar
                string resourceName = "InstallerSimple.context.exe"; // Nombre completo del recurso
                string destExePath = Path.Combine(installDir, exeName);
                ExtractResource(resourceName, destExePath);

                Console.WriteLine("Moviendo el ejecutable...");
                Console.WriteLine($"Ejecutable extraído a: {destExePath}");

                // Añadir al PATH
                Console.WriteLine("Añadiendo al PATH...");
                AddToPath(installDir);

                // Final bueno
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
    }
}
