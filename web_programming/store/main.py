from pypromptpay import qr_code

account_ = "0951847769"
path = 'C:/Users/Professor/Desktop/web_programming/media/qrcode/admin2022-03-25_10-40-04-040526.png' # Save picture to disk
money_ = "100.0"
currency_ = "THB"

qr_code(account=account_, one_time=True, path_qr_code = path ,country="TH",money=money_,currency=currency_)
