from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import QrCode

@login_required
def qrcode(response):
   if response.method == "POST":
      url = response.POST['url']
      QrCode.objects.create(url=url)

   qr_code = QrCode.objects.all()
   return render(response, "index.html", {
      'qr_code': qr_code
   })
