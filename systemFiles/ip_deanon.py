import socket
import threading
import requests
import ipaddress


class IpInfo:
    def __init__(self):
        self.ip = input('\n [+] IP For Scan: ')

        try:
            ipaddress.ip_address(self.ip)
        except ValueError:
            raise ValueError('IP адресс введён неверно')

        self.output()

    def defaultInfo(self):
        r = requests.get(f'http://ip-api.com/json/{self.ip}').json()

        return r

    def openPorts(self):
        openPortsList = []

        def scan_port(ip,port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            try:
                sock.connect((ip,port))
                openPortsList.append(str(port))
                sock.close()
            except:
                pass

        for i in range(65535):
            potoc = threading.Thread(target=scan_port, args=(self.ip, i))
            potoc.start()

        return openPortsList

    def output(self):
        default = self.defaultInfo()
        openPorts = self.openPorts()

        print(f''' =====================================
  IP adress:   {self.ip}
  Country:     {default["country"]}\n  CountryCode: {default["countryCode"]} 
  Region:      {default["region"]}\n  Region Name: {default["regionName"]}
  City:        {default["city"]}\n  Zip:         {default["zip"]}
  Latinude:    {default["lat"]}\n  Longitude:   {default["lon"]}
  Timezone:    {default["timezone"]}\n  ISP:         {default["isp"]}
  Org:         {default["org"]}\n  As:          {default["as"]}
  Open ports:  {', '.join(openPorts)}
 =====================================''')

        input()


def BSSIDinfo():
    print('\n ============================')
    query = input(f'  BSSID: ')
    try:
        response = requests.get(
            "https://api.mylnikov.org/geolocation/wifi?v=1.1&data=open&bssid=" + query)
        data = response.json()
        status = data["result"]
        if status == 200:
            lat = data["data"]["lat"]
            lon = data["data"]["lon"]
            print(f'  Latinude: {lat}\n  Longitude: {lon}')
            print(' =============================')
        else:
            errorCode = data["message"]
            errorMessage = data["desc"]
            print(
                f'  Error code: {errorCode}\n  Error message: {errorMessage}')
            print(' ============================')
    except:
        print(f' НАПИШИ ВЕРНО!')
    input()


def main():
    print(' Использование:\n n.IpInfo\n n.BSSIDinfo')


if __name__ == '__main__':
    main()
