def create_contextignore(contextignore_path):
    """Crea un archivo .contextignore con patrones comunes para ignorar archivos y carpetas."""

    contextignore_content = """# Ignorar todos los archivos de configuración
*.config
*.cfg
*.ini

# Ignorar archivos de log
*.log

# Ignorar archivos de salida o temporales
*.tmp
*.temp
*.out

# Ignorar archivos de caché
*.cache
*.pyc
__pycache__/

# Ignorar dependencias de proyecto
node_modules/
venv/
.venv/
.env
.Python

# Ignorar archivos generados por IDEs
.idea/
*.sublime-workspace
*.sublime-project
*.vscode/
*.swp

# Ignorar archivos de sistema operativo
.DS_Store
Thumbs.db

# Ignorar carpetas que pueden contener muchos archivos
dist/
build/
target/
out/

# Ignorar bases de datos y archivos relacionados
*.sqlite
*.sqlite3
*.db
*.db-journal
*.sql
*.bak
*.dump

# Ignorar archivos de virtualización y contenedores
docker-compose.override.yml
*.dockerfile
docker-sync.yml

# Ignorar archivos multimedia pesados
*.mp4
*.mov
*.avi
*.mkv
*.mp3
*.wav
*.flac
*.zip
*.tar.gz
*.rar
*.7z
*.iso
*.bin
*.csv
*.tsv
*.json
*.xml

# Ignorar archivos de configuración sensibles o credenciales
*.env
secrets.yml
.env.local
.env.production
.env.development
.env.test

# Ignorar archivos de depuración o análisis
*.trace
*.prof
*.log
*.dat
*.dmp
coverage/

# Ignorar archivos específicos de lenguajes o herramientas
# Ruby
*.gem
.ruby-version
.ruby-gemset
.bundle/
vendor/bundle/

# Pipenv y Poetry (Python)
Pipfile
Pipfile.lock
poetry.lock

# Maven y Gradle (Java)
.mvn/
target/
.gradle/
build/

# Rust/Cargo
target/
Cargo.lock

# Go Modules
go.sum
go.mod

# Composer (PHP)
vendor/
composer.lock

# Mix y rebar3 (Elixir/Erlang)
deps/
_build/

# Stack y Cabal (Haskell)
.stack-work/
dist-newstyle/
cabal.project.local

# Dart/Flutter
.dart_tool/
.packages
pubspec.lock
build/
.flutter-plugins
.flutter-plugins-dependencies

# Swift/Objective-C (CocoaPods y Carthage)
Pods/
Podfile.lock
Carthage/Build/

# .NET (C#)
bin/
obj/
*.csproj.user
*.suo
*.user
.vscode/
.nuget/
project.lock.json
project.fragment.lock.json

# Perl (Carton y local::lib)
local/
carton.lock

# R (renv)
.Rhistory
.RData
.Rproj.user/
renv/library/

# LaTeX
*.aux
*.bbl
*.blg
*.log
*.toc
*.out
*.lot
*.lof
*.gz

# Ignorar archivos y modelos de machine learning
*.h5
*.ckpt
*.pb
*.pth
*.pt
*.pkl
*.joblib
models/
data/

# Ignorar archivos temporales y de desarrollo
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.eslintcache
.prettiercache
.sass-cache/
coverage/

# Ignorar submódulos de Git
.gitmodules
.git/worktrees/
.git/

"""

    # Crear y escribir en el archivo .contextignore
    with open(contextignore_path, 'w', encoding='utf-8') as f:
        f.write(contextignore_content.strip())