#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# Android Studio AVD setup script for macOS (Apple Silicon)
# Device: Pixel_4
# Android: 11 (API 30)
# ABI: arm64-v8a
# rootAVD path: /Users/egor/rootAVD
# ------------------------------------------------------------

AVD_NAME="Pixel_4_API_30_ARM64"
DEVICE_ID="pixel_4"
PACKAGE="system-images;android-30;google_apis;arm64-v8a"
ROOTAVD_DIR="/Users/egor/rootAVD"

ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$HOME/Library/Android/sdk}"
CMDLINE_TOOLS_BIN=""
EMULATOR_BIN="$ANDROID_SDK_ROOT/emulator"
PLATFORM_TOOLS_BIN="$ANDROID_SDK_ROOT/platform-tools"

export ANDROID_SDK_ROOT
export PATH="$EMULATOR_BIN:$PLATFORM_TOOLS_BIN:$PATH"

log() {
  echo "[setup-avd] $*"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Ошибка: не найдена команда '$1'. Убедись, что Android SDK установлен." >&2
    exit 1
  fi
}

detect_cmdline_tools_bin() {
  local candidate=""

  if [ -x "$ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" ] && [ -x "$ANDROID_SDK_ROOT/cmdline-tools/latest/bin/avdmanager" ]; then
    candidate="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin"
  else
    candidate="$(find "$ANDROID_SDK_ROOT/cmdline-tools" -maxdepth 3 -type f -name sdkmanager 2>/dev/null | head -n 1 || true)"
    if [ -n "$candidate" ]; then
      candidate="$(dirname "$candidate")"
      if [ ! -x "$candidate/avdmanager" ]; then
        candidate=""
      fi
    fi
  fi

  echo "$candidate"
}

log "Проверка Android SDK в: $ANDROID_SDK_ROOT"
if [ ! -d "$ANDROID_SDK_ROOT" ]; then
  echo "Ошибка: каталог SDK не найден: $ANDROID_SDK_ROOT" >&2
  echo "Установи Android Studio + SDK, либо задай ANDROID_SDK_ROOT вручную." >&2
  exit 1
fi

CMDLINE_TOOLS_BIN="$(detect_cmdline_tools_bin)"
if [ -n "$CMDLINE_TOOLS_BIN" ]; then
  export PATH="$CMDLINE_TOOLS_BIN:$PATH"
else
  cat >&2 <<EOF
Ошибка: не найдены sdkmanager/avdmanager в Android SDK.

Скорее всего не установлен пакет "Android SDK Command-line Tools".
Установи его в Android Studio:
  Android Studio -> Settings -> Android SDK -> SDK Tools ->
  [x] Android SDK Command-line Tools (latest)

После установки запусти скрипт снова.
EOF
  exit 1
fi

require_cmd sdkmanager
require_cmd avdmanager

log "Принимаем лицензии SDK (может занять до минуты)"
yes | sdkmanager --licenses >/dev/null || true

log "Устанавливаем необходимые компоненты SDK"
sdkmanager \
  "platform-tools" \
  "emulator" \
  "platforms;android-30" \
  "$PACKAGE"

if avdmanager list avd | grep -q "Name: $AVD_NAME"; then
  log "AVD '$AVD_NAME' уже существует — пропускаем создание"
else
  log "Создаем AVD '$AVD_NAME' ($DEVICE_ID, API 30, arm64-v8a)"
  echo "no" | avdmanager create avd \
    --name "$AVD_NAME" \
    --package "$PACKAGE" \
    --device "$DEVICE_ID"
fi

AVD_DIR="$HOME/.android/avd/${AVD_NAME}.avd"
CONFIG_FILE="$AVD_DIR/config.ini"

if [ -f "$CONFIG_FILE" ]; then
  log "Настраиваем параметры AVD (производительность/совместимость)"

  set_config() {
    local key="$1"
    local value="$2"
    if grep -q "^${key}=" "$CONFIG_FILE"; then
      sed -i.bak "s|^${key}=.*|${key}=${value}|" "$CONFIG_FILE"
    else
      printf "%s=%s\n" "$key" "$value" >> "$CONFIG_FILE"
    fi
  }

  set_config "hw.cpu.ncore" "4"
  set_config "hw.ramSize" "4096"
  set_config "disk.dataPartition.size" "8192M"
  set_config "vm.heapSize" "256"
  set_config "hw.gpu.enabled" "yes"
  set_config "hw.gpu.mode" "host"
  set_config "fastboot.forceColdBoot" "yes"
  set_config "PlayStore.enabled" "false"
else
  echo "Ошибка: не найден config.ini у AVD: $CONFIG_FILE" >&2
  exit 1
fi

log "Проверяем наличие rootAVD: $ROOTAVD_DIR"
if [ ! -d "$ROOTAVD_DIR" ]; then
  echo "Внимание: rootAVD не найден по пути $ROOTAVD_DIR" >&2
  echo "AVD создан без root. Для root размести rootAVD в указанной папке и запусти скрипт снова." >&2
  exit 0
fi

ROOT_SCRIPT=""
if [ -f "$ROOTAVD_DIR/rootAVD.sh" ]; then
  ROOT_SCRIPT="$ROOTAVD_DIR/rootAVD.sh"
elif [ -f "$ROOTAVD_DIR/rootAVD" ]; then
  ROOT_SCRIPT="$ROOTAVD_DIR/rootAVD"
fi

if [ -z "$ROOT_SCRIPT" ]; then
  echo "Внимание: в $ROOTAVD_DIR не найден rootAVD.sh/rootAVD" >&2
  echo "AVD создан без root. Проверь установку rootAVD." >&2
  exit 0
fi

log "Запускаем rootAVD для '$AVD_NAME'"
chmod +x "$ROOT_SCRIPT"
(
  cd "$ROOTAVD_DIR"
  "$ROOT_SCRIPT" ListAllAVDs || true
  "$ROOT_SCRIPT" "$AVD_NAME"
)

cat <<MSG

Готово.
AVD: $AVD_NAME
Запуск эмулятора:
  emulator -avd $AVD_NAME

Если root не активировался сразу, сделай cold boot:
  emulator -avd $AVD_NAME -no-snapshot-load

MSG
