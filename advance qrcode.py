import qrcode
from PIL import image 
qr=qrcode.QRCODE(version=1,error-correction=qrcode.constants.Error-CORRECT-H,box-size=10,border=4)
qr.add-data("https://github.com/Albinzer")
qr.make(fit=True)
img=qr.make-image(fill-color="Dark-blue",back-color="Light-Gray")
img.save("Albinzer-Abs.png")
