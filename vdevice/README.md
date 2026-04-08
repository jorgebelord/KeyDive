# Virtual Android device setup (macOS / Apple Silicon)

Скрипт `setup_pixel4_api30_arm64.sh` автоматически:

1. Проверяет Android SDK.
2. Устанавливает компоненты для Android 11 (API 30, `arm64-v8a`).
3. Создаёт AVD `Pixel_4_API_30_ARM64` на базе устройства `Pixel_4`.
4. Применяет базовые настройки производительности в `config.ini`.
5. Пытается применить root через `rootAVD` из `/Users/egor/rootAVD`.

## Запуск

```bash
cd vdevice
./setup_pixel4_api30_arm64.sh
```

## Важно

- По умолчанию SDK ищется по пути:
  - `~/Library/Android/sdk`
- Если у тебя другой путь, укажи переменную окружения:

```bash
ANDROID_SDK_ROOT=/path/to/Android/sdk ./setup_pixel4_api30_arm64.sh
```
