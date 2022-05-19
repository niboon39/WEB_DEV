import cv2  as cv
from pytesseract import pytesseract 

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


dict_dt = {'ม.ค.' : '01',
           'ก.พ.' : '02',
           'มี.ค.' : '03',
           'เม.ย.' : '04',
           'พ.ค.' : '05',
           'มิ.ย.' : '06',
           'ก.ค.' : '07',
           'ส.ค.' : '08',
           'ก.ย.' : '09',
           'ต.ค.' : '10',
           'พ.ย.' : '11',
           'ธ.ค.' : '12'}

def list_to_str (s):
    new_date_time = " "
    return new_date_time.join(s)


def kbank (Slip_kbank ):
    ''' K_bank '''

    # resize image K_bank  
    # Fic size image (width = 1320 , height = 1074) 
    dim = (1074 , 1320) 
    resized = cv.resize(Slip_kbank, dim , interpolation = cv.INTER_AREA)
    # print(f"Resized Dimensions : {resized.shape}")
    # cv.imshow("resized" , resized)

    # Count : number of slip. 
    Output_kbank = ['','','']

    dtx1 , dtx2 , dty1 , dty2 = 38 , 451 , 83 , 155
    date_time =  resized[dty1:dty2 , dtx1:dtx2]
    # cv.imshow('date_time', date_time)
    
    nx1 , nx2 , ny1 , ny2 = 257 , 867 , 520 , 645
    name = resized[ny1:ny2 , nx1:nx2]
    # cv.imshow('name', name)

    ax1 , ax2 , ay1 , ay2 = 72 , 709 , 1023 , 1109
    amount = resized[ay1:ay2 , ax1:ax2]
    # cv.imshow('amount' , amount)

    # Verified by K+ 
    vx1 , vx2 , vy1 , vy2 = 721 , 1109 , 851 , 1251
    verified = resized[vy1:vy2 , vx1:vx2]
    # cv.imshow('verified' , verified)
    # status = cv.imwrite(f'C:/Users/Niboon/Desktop/storefront/read_qr_code/OCR/picture/Bank/verified_k_plus/verified{Count}.png', verified)
    # print("Image written to verified_K+ : ",status)

    # cv.waitKey(0)

    ''' Output string --> Check '''

    # Date_Time 
    date_in_img = pytesseract.image_to_string(date_time , 'tha')

    Output_kbank[0] += date_in_img[0:10]
    # print(date_in_img)

    time_in_img = date_in_img[10 : len(date_in_img)-3]
    Output_kbank[0] += time_in_img
    # print(time_in_img)
    
    # Name 
    name_in_img = pytesseract.image_to_string(name , 'tha')
    Output_kbank[1] += name_in_img.replace('\n', '')
    # print(name_in_img)

    # amount 
    amount_in_img = pytesseract.image_to_string(amount , 'tha')
    Output_kbank[2] += amount_in_img.replace('\n','').replace(",","")
    # print(amount_in_img)

    # cv.waitKey(0)

    new_out = Output_kbank[0].split()
    print(new_out)
    for key , item in dict_dt.items() : 
        if new_out[1] == key : 
            new_out[1] = item 
    new_out[2] = int( '25'+new_out[2] )
    # print(new_out[2])
    y = int(new_out[2]) - 543
    # print(y) 
    new_out[2] = str(y) 
    # print(new_out)
    new_dt = list_to_str(new_out)
    print(new_dt)
    Output_kbank[0] = new_dt
    return Output_kbank 


def SCB (Slip_scb ):

    '''  SCB  '''
    # resize image SCB 
    # Fic size image (width = 1024 , height = 1600) 
    dim = (1024 , 1600) 
    resized = cv.resize(Slip_scb, dim , interpolation = cv.INTER_AREA)
    # print(f"Resized Dimensions : {resized.shape}")
    # cv.imshow("resized" , resized)

    output_scb = ['' , '' , '']

    dtx1 , dtx2 , dty1 , dty2 = 341 , 677 , 377 , 436 
    data_time = resized[dty1:dty2,dtx1:dtx2  ]

    # cv.imshow("dtae and time" , data_time)

    ax1 , ax2 , ay1 , ay2 = 260 , 997 , 924 , 1024 
    amount = resized[ay1:ay2 , ax1:ax2 ]
    # cv.imshow('amount_scb' , amount)

    nx1 , nx2 , ny1 , ny2 = 598 , 995 , 709 , 792 
    name = resized[ny1:ny2 , nx1:nx2]
    # cv.imshow('name_scb' , name)


    # QR CODE Verified 
    qrx1 , qrx2 , qry1 , qry2 = 711 , 992 , 1046 , 1313
    qr_code_scb = resized[qry1:qry2 , qrx1:qrx2]
    # cv.imshow("qr_code_scb" , qr_code_scb)
    # status = cv.imwrite(f'C:/Users/Niboon/Desktop/storefront/read_qr_code/OCR/picture/Bank/verified_scb/verified{Count}.png', qr_code_scb)
    # print("Image written to verified_SCB : ",status)

    date_time_in_img =  pytesseract.image_to_string(data_time , 'tha')
    # print(date_time_in_img)
    date_time_in_img = date_time_in_img.replace("-" , "")
    output_scb[0] += date_time_in_img.replace("\n","")

    amount_in_img = pytesseract.image_to_string(amount , 'tha')
    # print(amount_in_img)
    output_scb[2] += amount_in_img.replace("\n" , "").replace("," , "")
    output_scb[2] += ' บาท'


    name_in_img =  pytesseract.image_to_string(name , 'tha')
    # print(name_in_img)
    output_scb[1] += name_in_img.replace("\n" , "")

    # print(output_scb)

    # cv.waitKey(0)

    new_out = output_scb[0].split()
    # print(new_out)
    for key , item in dict_dt.items() : 
        if new_out[1] == key : 
            new_out[1] = item 
    new_out[2] = str(int(new_out[2]) - 543 )
    # print(new_out) 
    # # print(new_out)
    new_dt = list_to_str(new_out)
    # # print(new_dt)
    # Output_kbank[0] = new_dt
    output_scb[0] = new_dt
    return output_scb


def krungthai (Slip_krungthai ):

    ''' Krungthai '''
    # resize image SCB 
    # Fic size image (width = 1024 , height = 1600) 
    dim = (1074 , 1297) 
    resized = cv.resize(Slip_krungthai, dim , interpolation = cv.INTER_AREA)
    # print(f"Resized Dimensions : {resized.shape}")
    # cv.imshow("resized" , resized)

    output_krungthai = ['','','']

    dtx1 , dtx2 , dty1 , dty2 = 571 , 1074 , 1122 , 1208 
    date_time =  resized[dty1:dty2 , dtx1:dtx2] 
    # cv.imshow('date_time', date_time)

    nx1 , nx2 , ny1 , ny2 = 181 , 913 , 698 , 762 
    name = resized[ny1:ny2 , nx1:nx2]
    # cv.imshow('name' , name )

    ax1 , ax2 , ay1 , ay2 = 257 , 1057 , 924 , 1028 
    amount = resized[ay1:ay2 , ax1:ax2]
    # cv.imshow('amount' , amount)

    # QR code 
    qrx1 , qrx2 , qry1 , qry2 = 811 , 1039 , 256 , 476 
    qr_code_krungthai = resized[qry1:qry2 , qrx1:qrx2]
    # cv.imshow('qr_code' , qr_code_krungthai)
    # status = cv.imwrite(f'C:/Users/Niboon/Desktop/storefront/read_qr_code/OCR/picture/Bank/verified_krungthai/verified{Count}.png', qr_code_krungthai)
    # print("Image written to verified_Krungthai : ",status)


    date_time_in_img = pytesseract.image_to_string(date_time , 'tha')
    # print(date_time_in_img)
    output_krungthai[0] += date_time_in_img.replace("-","").replace("\n","")

    name_in_img = pytesseract.image_to_string(name , 'tha')
    # print(name_in_img)
    output_krungthai[1] += name_in_img.replace("\n" , "")

    amount_in_img = pytesseract.image_to_string(amount , 'eng')
    # print(amount_in_img)
    output_krungthai[2] += amount_in_img.replace("\n","").replace("uin", "บาท").replace(",","")

    # print(output_krungthai)
    # cv.waitKey(0)

    new_out = output_krungthai[0].split()
    # print(new_out)
    for key , item in dict_dt.items() : 
        if new_out[1] == key : 
            new_out[1] = item 
    new_out[2] = str(int(new_out[2]) - 543 )
    # print(new_out) 
    # # # print(new_out)
    new_dt = list_to_str(new_out)
    # # print(new_dt)
    # Output_kbank[0] = new_dt
    output_krungthai[0] = new_dt


    return output_krungthai


def check_all (bank,img_upload , date_time , name , amount):
    checksum = 0 
    if bank == 'K':
        output_k = kbank(Slip_kbank = img_upload)
        if date_time == output_k[0]: 
            checksum+=1 
            print("PASS") 
        
        else: 
            print("Wrong date_time.")

        if name[0] == output_k[1] or name[1] == output_k[1]: 
            checksum +=1 
            print("PASS")

        else: print("Wrong name.")

        if amount == output_k[2] :
            checksum+=1 
            print("PASS")

        else: print("Wrong amount.")

    elif bank == 'S' : 
        output_scb = SCB(Slip_scb = img_upload)
        if date_time == output_scb[0]:
            checksum+=1 
            print("PASS")
        else: print("Wrong date_time.")

        if name[0] == output_scb[1] or name[1] == output_scb[1]:
            checksum+=1 
            print("PASS")
        else: print("Wrong name.")

        if amount == output_scb[2] :
            checksum+=1 
            print("PASS")
        else: print("Wrong amount.")

    elif bank == 'T':
        output_krungthai = krungthai(Slip_krungthai = img_upload)
        if date_time == output_krungthai[0]:
            checksum+=1 
            print("PASS")
        else: print("Wrong date_time.")

        if name[0] == output_krungthai[1] or name[1] == output_krungthai[1]:
            checksum+=1 
            print("PASS")
        else: print("Wrong name.")

        if amount == output_krungthai[2] :
            checksum+=1 
            print("PASS")
        else: print("Wrong amount.")

    else:
        print("Bank not found ...")

    if checksum == 3 : 
        return True
    else:
        return False


if __name__ == "__main__":
    pass 
    # Read image 
    # path_kbank = "C:\\Users\\Niboon\\Desktop\\storefront\\read_qr_code\\OCR\\picture\\bank\\Kbank\\Kbank2.jpg"
    # path_scb = "C:\\Users\\Niboon\\Desktop\\storefront\\read_qr_code\\OCR\\picture\\bank\\SCB\\SCB.jpg"
    # path_krungthai = "C:\\Users\\Niboon\\Desktop\\storefront\\read_qr_code\\OCR\\picture\\Bank\\Krungthai\\Krungthai.jpg"
    # img = cv.imread(path_kbank , cv.IMREAD_UNCHANGED)
    # print(f"Original Dimensions : {img.shape}")

    # print(kbank(img ))
    # print(SCB(img , 2))
    # print(krungthai(img))

    # main(bank = "kasikorn", img_upload = img, date_time = '6 ธ.ค. 64 15:17 ' , name = 'นาง วาสนา สุขแจ่ม', amount = "100.00 บาท", count = 0 )
    
   