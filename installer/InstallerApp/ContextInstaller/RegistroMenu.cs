using Microsoft.Win32;
using System;
using System.IO;
using System.Reflection;

namespace ContextInstaller
{
    class RegistroMenu
    {
        public static void CrearMenuCascada()
        {
            // Definir la clave donde se creará el menú en cascada
            string clickDirectorio = @"HKEY_CLASSES_ROOT\Directory\shell\CascadeMenu";

            string clickArchivo = @"HKEY_CLASSES_ROOT\*\Shell\CascadeMenu";

            string clickFondo = @"HKEY_CLASSES_ROOT\Directory\Background\Shell\CascadeMenu";

            try
            {
                // Extraer el icono incrustado y guardarlo temporalmente
                string iconoPath = ExtraerIconoIncrustado();

                if (iconoPath == null)
                {
                    Console.WriteLine("No se pudo extraer el icono.");
                    return;
                }

                // ----------------------------  Click sobre directorio

                // ----------------------------  Click sobre directorio
                Registry.SetValue(clickDirectorio, "MUIVerb", "Context");
                Registry.SetValue(clickDirectorio, "Icon", iconoPath);
                Registry.SetValue(clickDirectorio, "SubCommands", "context;contextIA;contextCheck;contextList;contextInit");

                // ------------------------------  Click sobre fondo directorio
                Registry.SetValue(clickFondo, "MUIVerb", "Context");
                Registry.SetValue(clickFondo, "Icon", iconoPath);
                Registry.SetValue(clickFondo, "SubCommands", "context;contextIA;contextCheck;contextList;contextInit");

                // ------------------------------  Click sobre archivo
                Registry.SetValue(clickArchivo, "MUIVerb", "Context");
                Registry.SetValue(clickArchivo, "Icon", iconoPath);
                Registry.SetValue(clickArchivo, "SubCommands", "contextAdd");



                // Crear la subclave para el comando personalizado 1 (ejecutar "context" desde el PATH)
                string comandoPersonalizado1 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\context";
                Registry.SetValue(comandoPersonalizado1, "", "context");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado1 + @"\command", "", @"cmd.exe /c cd ""%V"" && context");

                // Crear la subclave para el comando personalizado 2 (context add)
                string comandoPersonalizado2 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\contextAdd";
                Registry.SetValue(comandoPersonalizado2, "", "context add");

                // Aquí pasamos %1 directamente, lo que permite que el contexto sea el archivo que se ha clicado
                Registry.SetValue(comandoPersonalizado2 + @"\command", "", @"cmd.exe /c context add ""%1""");


                // Crear la subclave para el comando personalizado 3 (context ia)
                string comandoPersonalizado3 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\contextIA";
                Registry.SetValue(comandoPersonalizado3, "", "context ia");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado3 + @"\command", "", @"cmd.exe /c cd ""%V"" && context ia");

                // Crear la subclave para el comando personalizado 4 (context list)
                string comandoPersonalizado4 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\contextList";
                Registry.SetValue(comandoPersonalizado4, "", "context list");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado4 + @"\command", "", @"cmd.exe /c cd ""%V"" && context list");

                // Crear la subclave para el comando personalizado 5 (context check)
                string comandoPersonalizado5 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\contextCheck";
                Registry.SetValue(comandoPersonalizado5, "", "context check");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado5 + @"\command", "", @"cmd.exe /c cd ""%V"" && context check");

                // Crear la subclave para el comando personalizado 6 (context init)
                string comandoPersonalizado6 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\contextInit";
                Registry.SetValue(comandoPersonalizado6, "", "context init");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado6 + @"\command", "", @"cmd.exe /c cd ""%V"" && context init");


                Console.WriteLine("Menú en cascada creado exitosamente con el icono incrustado.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al crear el menú en cascada: {ex.Message}");
            }
        }

        private static string ExtraerIconoIncrustado()
        {
            try
            {
                // Obtener el ensamblado actual
                Assembly ensamblado = Assembly.GetExecutingAssembly();

                // Nombre del recurso incrustado (debe coincidir con el nombre en tu ensamblado)
                string nombreRecurso = "ContextInstaller.icon.ico";

                // Ruta temporal donde guardar el icono
                string rutaTemporal = Path.Combine(Path.GetTempPath(), "context_menu_icon.ico");

                // Extraer el recurso incrustado y guardarlo como archivo temporal
                using (Stream stream = ensamblado.GetManifestResourceStream(nombreRecurso))
                {
                    if (stream == null) return null;

                    using (FileStream archivoTemp = new FileStream(rutaTemporal, FileMode.Create))
                    {
                        stream.CopyTo(archivoTemp);
                    }
                }

                return rutaTemporal;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al extraer el icono incrustado: {ex.Message}");
                return null;
            }
        }
    }
}