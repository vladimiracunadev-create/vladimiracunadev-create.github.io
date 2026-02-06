#!/bin/bash

# Script para corregir la versión de Java en el entorno local

echo "Verificando versiones de Java instaladas..."
/usr/libexec/java_home -V

JAVA_17_PATH=$(/usr/libexec/java_home -v 17 2>/dev/null)

if [ -z "$JAVA_17_PATH" ]; then
    echo "ERROR: Java 17 no fue detectado. Por favor instálalo con:"
    echo "brew install --cask temurin@17"
    exit 1
fi

echo "Java 17 detectado en: $JAVA_17_PATH"

# Sugerir exportación al usuario
echo ""
echo "Para usar Java 17 en esta sesión, ejecuta:"
echo "export JAVA_HOME=\$JAVA_17_PATH"
echo ""
echo "Para hacerlo permanente en tu terminal (ZSH), ejecuta:"
echo "echo 'export JAVA_HOME=\$(/usr/libexec/java_home -v 17)' >> ~/.zshrc"
echo "source ~/.zshrc"

# Intentar configurar para la sesión actual del proceso
export JAVA_HOME=$JAVA_17_PATH
java -version
