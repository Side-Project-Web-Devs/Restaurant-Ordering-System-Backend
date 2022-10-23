from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import QrCode


@login_required
def qrcode(response):
    if response.method == "POST":
        url = response.POST['url']
        QrCode.objects.create(url=url)
        messages.success(response, "QR code generated!")

    qr_code = QrCode.objects.all()
    return render(response, "index.html", {
        'qr_code': qr_code
    })


def delete_qr(response, id):
    qr = get_object_or_404(QrCode, id=id)
    qr.delete()
    messages.error(response, "QR code successfully deleted!")
    return redirect('qrcode_generator')
