import time
import pywifi

def sniff_wifi_ssid():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Puedes ajustar esto según tu configuración

    print("Escaneando redes Wi-Fi...")
    iface.scan()
    time.sleep(10)
    scan_results = iface.scan_results()

    if not scan_results:
        print("No se encontraron redes Wi-Fi.")
        return

    print("Redes Wi-Fi encontradas:")
    for result in scan_results:
        ssid = result.ssid
        print(f"SSID: {ssid}")

# Uso del método
sniff_wifi_ssid()
