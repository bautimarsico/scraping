from bs4 import BeautifulSoup
import requests
import csv

#-------------- cantidad de paginas a scrapear ------------
paginas = 20
#-------------- valor minimo de descuento ----------------
discount = 60


#---------------------------------------------------------
with open("ofertas.csv","w") as file:
    csvwriter = csv.writer(file, delimiter=',')
    fields = ['Producto', 'Precio', 'Descuento', 'Url']
    csvwriter.writerow(fields)
    
    for i in range(1,paginas):
        url = requests.get(f"https://www.mercadolibre.com.ar/ofertas?container_id=MLA779357-3&page={i}")
        soup = BeautifulSoup(url.text,"html.parser")
        container = soup.find_all(class_="promotion-item")

        for c in container:
            descuento = c.find(class_ = "promotion-item__discount-text").text
            descuento = descuento[:2]
            if descuento != "":
                if str(descuento).isnumeric() == False :
                    descuento = int(descuento[0])
                else:
                    descuento = int(descuento)
                if descuento >= discount:
                    url = c.find(class_="promotion-item__link-container").get("href")
                    producto = c.find(class_="promotion-item__title").text
                    precio = c.find(class_="andes-money-amount__fraction").text
                    
                    row = [producto,precio,f"{descuento}%",url]
                    
                    csvwriter.writerow(row)
                    
