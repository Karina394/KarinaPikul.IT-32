import qrcode

print("Karina Pikul, IT-32")

contact = """BEGIN:VCARD
VERSION:3.0
FN:Karina Pikul
EMAIL:karinapikul0@gmail.com
END:VCARD"""

img = qrcode.make(contact)
img.save("contact.png")

print("QR-код збережено у файлі contact.png")
