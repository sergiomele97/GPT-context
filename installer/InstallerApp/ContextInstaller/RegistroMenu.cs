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
            string claveBase = @"HKEY_CLASSES_ROOT\Directory\shell\CascadeMenu";

            try
            {
                // Extraer el icono incrustado y guardarlo temporalmente
                string iconoPath = ExtraerIconoIncrustado();

                if (iconoPath == null)
                {
                    Console.WriteLine("No se pudo extraer el icono.");
                    return;
                }

                // Crear la clave para el menú en cascada y asignar el nombre
                Registry.SetValue(claveBase, "MUIVerb", "Context");

                // Agregar el icono personalizado al menú
                Registry.SetValue(claveBase, "Icon", iconoPath);

                // Definir los comandos del submenú
                Registry.SetValue(claveBase, "SubCommands", "context;contextAdd;contextIA");

                // Crear la subclave para el comando personalizado 1 (ejecutar "context" desde el PATH)
                string comandoPersonalizado1 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\context";
                Registry.SetValue(comandoPersonalizado1, "", "context");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado1 + @"\command", "", @"cmd.exe /c cd ""%V"" && context");

                // Crear la subclave para el comando personalizado 2 (context add)
                string comandoPersonalizado2 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\contextAdd";
                Registry.SetValue(comandoPersonalizado2, "", "context add");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado2 + @"\command", "", @"cmd.exe /c cd ""%V"" && context add");

                // Crear la subclave para el comando personalizado 3 (context ia)
                string comandoPersonalizado3 = @"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell\contextIA";
                Registry.SetValue(comandoPersonalizado3, "", "context ia");
                // Ejecutar en la carpeta donde se hizo clic derecho
                Registry.SetValue(comandoPersonalizado3 + @"\command", "", @"cmd.exe /c cd ""%V"" && context ia");

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
