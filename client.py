import requests

url = 'http://172.20.10.2:5000'

def main():
    response = requests.get(url)
    if response.status_code == 200:
        print("Respuesta  del servidor")
        print(response.text)
    else:
        print("Error al conectar al servidor")
if __name__ == "__main__":
    main()

