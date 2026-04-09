import requests
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import base64
import json

# Конфигурация из window.VHX.config
VIDEO_ID = "1298930"
EMBED_URL = "https://embed.vhx.tv/videos/1298930?api=1&auth-user-token=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo3OTA4MjUzMiwiZXhwIjoxNzc1NzA3MDQzfQ.4TD42tfXgmR-mnN3CCryAO5D61CetvExgOQChD2OOtY&autoplay=1&collection_id=262686&color=e02d00&context=https%3A%2F%2Fwww.ntathome.com%2Fangels-in-america-part-one-millenium-approaches&is_trailer=false&live=0&locale=en&playsinline=1&product_id=72362&referrer=https%3A%2F%2Fwww.ntathome.com%2Fangels-in-america-part-one-millenium-approaches&vimeo=1"
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ2YmZlZmMzNGIyNTdhYTE4Y2E2NDUzNDE2ZTlmZmRjNjk4MDAxMDdhZTQ2ZWJhODg0YTU2ZDBjOGQ4NTYzMzgifQ.eyJhcHBfaWQiOjEyMDcwOSwiZXhwIjoxNzc1NzA3MDQzLCJub25jZSI6IjgxZjg0MzhhOWYwYTA5NDAiLCJzY29wZXMiOlsicHVibGljIl0sInNlc3Npb25faWQiOiJia2RRbjAxRmoxZmRlTmNlVkhUOWd3PT0iLCJzaXRlX2lkIjoxMTI0ODEsInVzZXJfaWQiOjc5MDgyNTMyfQ.wEN7aTMtUisz7OXrq47jUjvkscQMAwaYOrJEj_yDtw9UW_hs6ua2kyXeHXA_2fOMR7i2TyDhHOVtgUCJZV1bg2MJJuTXrM-cldu-Hr38x80CPqYHgn9M2VGqBzdyStL60wNPpYIowEbRK8n_RiVqukU3-vfx1PG-JE1wPfHIe8HVsRNXlTl93kmMqm9kg5o0DzBCVONa2deXppqzC_BqN5jFEo8sSRP7Ck4_nbk4XVHj2V-I-_dmejOIZMDsCzbFzMc1VJhjQQt7lDnCOk5xKFIsoAqrSj1DKbA-h21HZhpgcgileXI7z_ca6XPi8bpM5qs7bdT0_Wz7Vt73z7BvivaitHgsCOgod2bfh0mG5N8_MXH8ltcZS-ff8gyCD-r6AiHGDygpsyn0qsxox-_LCdJTrbJwEMqI9VTtxVcK-ncVt9b3HPd-3AX4UW9Ux1Zz8AhuRldygRfKiZarrJtX2F3Hp0BLLIRjq9AF6fTQkIkfVX5nlGJsqeaXBkf75XMtzCyr7iKUvRh3hO_c9z8RaqzBt2iEElcSFrAANqbW9O9rjzSrlaZK-J5TVdiz8wqdRY7TtpIsZYud0UEjKPBlXu-BrpqFpgoVsvgjFI2CkwZPUKGsx9akfWtBjbkRMXuom9WYkAfhSMwuqg6elpu0fKSAnIH3Q85wBzAGgexQseU"



# Ваш PSSH (из DevTools)
PSSH_BASE64 = "CAESoBEKzxAIARKeDQreBQgCEiCbQ0Cv6d1SXsmxHkdmEGlDS2kpipUKwWYUjZtVB3zw+Rio3dvOBiKOAjCCAQoCggEBAMjlrtBIz9FJ46W4kIr+k33S29SA4VYOYyi5GpoczbNcGAjUxxllxwiJICuLtO+TZ2HnBg3EW0WjXm0f+4FUTYYSFsp16vssucfERcLoinkOmJ53RIzTOiPIPEzEiexHPjUTps6LsZVBFTJRe6IaGQFEkKmVClAOuOXh0abdB8grWqNX9tcR7utZyv9TdpvGf0bNvWDfNmnWH1f7UK8M0YsE5Ubj+ma3dM72+E3esZB6xuRbZ5WHKvAvIc+6V/mQO+UQJvyiMKPuweEAGQw3LuFiV1PlVpPWiz06TmN7IIlvH1DBGpmelXXwCAoyfrd8FHpTV38VJrlxRIoa5e5SPdcCAwEAASi+sAFIAVKaAwgBEAAa8QIESiSPB/sCSn8ynovLzUZGlq+ZgmPKbj7beuxkP7CGv0kc4+JmzwC5GmaRRy+NXtdKuXKCxX7F5EWFv8WAQGUMAdIDV2bIQyQnOUc28"



# URL лицензии (замените на актуальный из DevTools)
LICENSE_URL = "https://player.vimeo.com/video/860743805/license/widevine?asset_id=860743805&s=1775745453-a1afb7b46a175a650b79b636cd93b5adfacc9bb02a7703ad6249699dff522d14&version=derived&atid=1506201421.1775699845&referrer=https%3A%2F%2Fwww.ntathome.com%2Fangels-in-america-part-one-millenium-approaches&first_log=1&player_location=onsite&playback_route=player_embed_ott"


# Заголовки запроса
HEADERS = {
    "Referer": "https://www.ntathome.com/angels-in-america-part-one-millenium-approaches",
    "Origin": "https://embed.vhx.tv",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/json"
}


def get_widevine_license():
    """Получение лицензии Widevine для DRM‑видео"""

    # Инициализация CDM
    cdm = Cdm.from_device(Device.load("/path/to/your/device.wvd"))

    # Декодирование PSSH
    pssh = PSSH(base64.b64decode(PSSH_BASE64))


    # Генерация запроса на лицензию
    challenge = cdm.get_license_challenge(pssh)

    # Отправка запроса на сервер лицензий
    response = requests.post(
        LICENSE_URL,
        headers=HEADERS,
        data=challenge,
        timeout=30
    )

    if response.status_code != 200:
        print(f"Ошибка:
    ЗДЕСЬ ОБРЫВ
    def get_widevine_license():
    """Получение лицензии Widevine для DRM‑видео"""


    # Инициализация CDM
    cdm = Cdm.from_device(Device.load("/path/to/your/device.wvd"))

    # Декодирование PSSH
    pssh = PSSH(base64.b64decode(PSSH_BASE64))


    # Генерация запроса на лицензию
    challenge = cdm.get_license_challenge(pssh)


    # Отправка запроса на сервер лицензий
    response = requests.post(
        LICENSE_URL,
        headers=HEADERS,
        data=challenge,
        timeout=30
    )

    if response.status_code != 200:
        print(f"Ошибка: HTTP {response.status_code}")
        print("Ответ сервера:", response.text)
        return None

    # Обработка ответа с лицензией
    license_data = response.content
    cdm.parse_license(pssh, license_data)

    # Получение ключей расшифровки
    keys = cdm.decrypt_keys(pssh)
    decryption_keys = {}

    for key in keys:
        if key.type == 'CONTENT':
            print(f"Найден ключ расшифровки: KID={key.kid.hex()}, KEY={key.key.hex()}")
            decryption_keys[key.kid.hex()] = key.key.hex()

    return decryption_keys


def main():
    print("Начинаем процесс получения лицензии Widevine...")

    try:
        keys = get_widevine_license()
        if keys:
            print("\n=== Успешно получены ключи расшифровки ===")
            for kid, key in keys.items():
                print(f"KID: {kid}")
                print(f"KEY: {key}")
                print("-" * 40)

            # Сохранение ключей в файл
            with open("decryption_keys.json", "w") as f:
                json.dump(keys, f, indent=2)
            print("Ключи сохранены в файл decryption_keys.json")
        else:
            print("Не удалось получить ключи расшифровки")
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()

