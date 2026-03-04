import requests as r

# my_ip = r.get("https://api.ipify.org", timeout=10).text
# print(f"🌍 Мой публичный IP: {my_ip}")
#
# for ip in ["37.203.37.94", "173.245.49.151", "141.101.121.51", "23.227.39.129"]:
#     try:
#         res = r.get(f"http://{ip}:80", timeout=10)
#         print(f"Поменял  IP: {res}")
#         print(f"✅ {ip} → {res.status_code}")
#     except:
#         print(f"❌ {ip} → недоступен")
#     # 🔌 Соединение закрывается автоматически



import requests

proxy_url = "5.252.33.13:2025"
# Если прокси требует логин/пароль:
# proxy_url = "http://user:password@37.203.37.188:8080"

proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

try:
    # Пытаемся зайти на внешний ресурс ЧЕРЕЗ прокси
    response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
    print(f"✅ Прокси работает! Ваш IP для внешнего мира: {response.text}")
except requests.exceptions.ProxyError:
    print("❌ ProxyError: Прокси доступен, но отклоняет запрос (проверьте логин/пароль или тип прокси).")
except requests.exceptions.ConnectTimeout:
    print("❌ ConnectTimeout: Нет сетевого соединения с сервером прокси (см. пункт 1 и 2).")
except Exception as e:
    print(f"❌ Ошибка: {e}")