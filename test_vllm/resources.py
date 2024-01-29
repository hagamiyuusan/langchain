birth_schema = """
{
    "personal_information": {
        "full_name": "Complete name of the individual as recorded on the birth certificate",
        "date_of_birth": {
            "numeric": "Birth date in numerical format (day/month/year)",
            "textual": "Birth date written out in words"
        },
        "gender": "Gender of the individual as recorded on the birth certificate",
        "ethnicity": "Ethnic group of the individual as recorded",
        "nationality": "Nationality of the individual as recorded",
        "place_of_birth": "Place where the individual was born",
        "hometown": "Registered hometown of the individual"
    },
    "mother_information": {
        "full_name": "Complete name of the mother",
        "year_of_birth": "Birth year of the mother",
        "ethnicity": "Ethnic group of the mother",
        "nationality": "Nationality of the mother",
        "residence": "Current place of residence of the mother"
    },
    "father_information": {
        "full_name": "Complete name of the father",
        "year_of_birth": "Birth year of the father",
        "ethnicity": "Ethnic group of the father",
        "nationality": "Nationality of the father",
        "residence": "Current place of residence of the father"
    },
    "registration_information": {
        "registrar_name": "Name of the person who registered the birth",
        "registration_location": "Location where the birth was registered",
        "registration_date": "Date when the birth was registered"
    },
    "certificate_issuer": {
        "issued_by": "Authority that issued the birth certificate",
        "issue_date": "Date when the birth certificate was issued",
        "document_number": "Specific number of the birth certificate issue"
    }
}
"""
birth_examples = """
	Input: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc thái Số: 158 GIẤY KHAI SINH (BÁN SAO) Họ, chữ đệm, tên: huỳnh thị tú trinh Ngày, tháng, năm sinh: 01/01/1990 - ghi bằng chữ: Ngày một, tháng một, năm một ngàn chín trăm chín mươi - Giới tính: Nữa Dân tộc: Kinh Quốc tịch: Việt Nam Nơi sinh: Bảo sanh Long Đất, tỉnh Bà Rịa - Vũng Tàu Quê quán: Số định danh cá nhân: Họ, chữ đệm, tên người mẹ: bùi THị TỐT Năm sinh: 1968 Dân tộc: Kinh Quốc tịch: Việt Nam Xã Nơi cư trú: Áp Thanh Long, xã Phước Thạnh, huyện Long Đất, tỉnh Bà Rịa ? Vũng Tàu Nhà Nhau Họ, chữ đệm, tên người cha: huỳnh văn sa Năm sinh: 1967 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Áp. Tường Thành, xã Phước Long Thọ, huyện Long Đất, tỉnh Bà Rịa ? Vũng Tàu Họ, chữ đệm, tên người đi khai sinh: Giấy tờ tùy thân: Nơi đăng ký khai sinh: Ủy ban nhân dân xã Phước Long Thọ, huyện Long Đất, tỉnh Bà Rịa Nhà Nhà Nhiều Vũng Tàu Ngày, tháng, năm đăng ký: 19/8/1996 NGƯỜI KÝ GIÁY KHAI SINH (Đã ký) Sao từ Sổ đăng ký khai sinh TỈNH BÀ RỊA - VŨNG TÀU Đất Đỏ, ngày 0 9 tháng 6 năm 2023 HUBND HUYỆN ĐẤT ĐỎ NGƯỜI KÝ Thuật (Ký, ghi rõ họ, tên, chức vụ và đóng dấu) Số: 69/GKS-BS KT. CHỦ TỊCH PHÓ CHỦ TỊCH BÊN ĐÁ Bằng Như Vàng Trị 
	Output:``` {
    "personal_information": {
        "full_name": "huỳnh thị tú trinh",
        "date_of_birth": {
            "numeric": "01/01/1990",
            "textual": "Ngày một, tháng một, năm một ngàn chín trăm chín mươi"
        },
        "gender": "Nữ",  
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "place_of_birth": "Bảo sanh Long Đất, tỉnh Bà Rịa - Vũng Tàu",
        "hometown": "Áp Thanh Long, xã Phước Thạnh, huyện Long Đất, tỉnh Bà Rịa - Vũng Tàu"
    },
    "mother_information": {
        "full_name": "bùi THị TỐT",
        "year_of_birth": "1968",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "residence": "Áp Thanh Long, xã Phước Thạnh, huyện Long Đất, tỉnh Bà Rịa - Vũng Tàu"
    },
    "father_information": {
        "full_name": "huỳnh văn sa",
        "year_of_birth": "1967",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "residence": "Áp Tường Thành, xã Phước Long Thọ, huyện Long Đất, tỉnh Bà Rịa - Vũng Tàu"
    },
    "registration_information": {
        "registrar_name": "Thuật",
        "registration_location": "Ủy ban nhân dân xã Phước Long Thọ, huyện Long Đất, tỉnh Bà Rịa",
        "registration_date": "19/8/1996"
    },
    "certificate_issuer": {
        "issued_by": "HUBND HUYỆN ĐẤT ĐỎ",
        "issue_date": "09/06/2023",
        "document_number": "69/GKS-BS"
    }
} ```

	Input: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc Số: 390 GIẤY KHAI SINH (BẢN SAO) Họ, chữ đệm, tên: NGUYỄN VĂN LỢI Ngày, tháng, năm sinh: 02/7/1990 - ghi bằng chữ: Ngày hai, tháng bảy, năm một ngàn chín trăm chín mươi Giới tính: Nam Dân tộc: Kinh Quốc tịch: Việt Nam Nơi sinh: Trạm xá Phước Hải, huyện Long Đất, tỉnh Đồng Nai Quê quán Số định danh cá nhân: Họ, chữ đệm, tên người mẹ: PHAN THỊ Được Năm sinh: 1963 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Áp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Họ, chữ đệm, tên người cha: nguyễn qua Năm sinh: 1959 - Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Ấp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Họ, chữ đệm, tên người đi khai sinh: Giấy tờ tùy thân: Thuật Nơi đăng ký khai sinh: Ủy ban nhân dân xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Nhân Thuận Ngày, tháng, năm đăng ký: 07/8/1990 NGƯỜI KÝ GIẤY KHAI SINH (Đã ký) Sao từ Sổ đăng ký khai sinh TỈNH BÀ RỊA - VŨNG TÀU Đất Đỏ, ngày 09 tháng 6 năm 2023 UBND HUYỆN ĐẤT ĐỎ NGƯỜI KÝ (Kỷ, ghi rõ họ, tên, chức vụ và đóng dấu) Số: 20/GKS-BS KT. CHỦ TỊCH PHÓ CHỦ TỊCH VIỆN ĐA Như Vàng 
	Output:``` {
    "personal_information": {
        "full_name": "NGUYỄN VĂN LỢI",
        "date_of_birth": {
            "numeric": "02/7/1990",
            "textual": "Ngày hai, tháng bảy, năm một ngàn chín trăm chín mươi"
        },
        "gender": "Nam",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "place_of_birth": "Trạm xá Phước Hải, huyện Long Đất, tỉnh Đồng Nai",
        "hometown": ""
    },
    "mother_information": {
        "full_name": "PHAN THỊ Được",
        "year_of_birth": "1963",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "residence": "Áp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai"
    },
    "father_information": {
        "full_name": "nguyễn qua",
        "year_of_birth": "1959",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "residence": "Ấp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai"
    },
    "registration_information": {
        "registrar_name": "Thuật Nhân Thuận",
        "registration_location": "Ủy ban nhân dân xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai",
        "registration_date": "07/8/1990"
    },
    "certificate_issuer": {
        "issued_by": "UBND HUYỆN ĐẤT ĐỎ",
        "issue_date": "09/06/2023",
        "document_number": "20/GKS-BS"
    }
} ```
	Input: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc Số: 178 GIẤY KHAI SINH (BÁN SAO) Xã Họ, chữ đệm, tên: đặng minh lai nam Ngày, tháng, năm sinh: 09/12/1984 - ghi bằng chữ: Ngày chín, tháng mười hai, năm một ngàn chín trăm tám mươi tư này Giới tính: Nam Dân tộc: Kinh Quốc tịch: Việt Nam Xã Nơi sinh: Xã Phước Hải, huyện Long Đất, tỉnh Đồng Nai Nam Quê quán: Số định danh cá nhân: Họ, chữ đệm, tên người mẹ: Đặng THị MIÊN Năm sinh: 1965 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Ấp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tinh Đồng Nai Họ, chữ đệm, tên người cha: nguyễn văn hải Năm sinh: 1963 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Áp Phước Thới, xã Phước Long Thọ, huyện Long Đất, tỉnh Đồng Nai Xã Họ, chữ đệm, tên người đi khai sinh: nhau Giấy tờ tùy thân: Nơi đăng ký khai sinh: Ủy ban nhân dân xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Ngày, tháng, năm đăng ký: 26/5/1986 NGƯỜI KÝ GIẤY KHAI SINH (Đã ký) TỈNH BÀ RỊA - VŨNG TÀU Sao từ Sổ đăng ký khai sinh 19 Đất Đỏ, ngày 09 tháng 6 năm 2023 UBND HUYỆN ĐẤT ĐỎ NGƯỜI KÝ (Ký, ghi rõ họ, tên, chức vụ và đóng dấu) Số: 76/GKS-BS KT.CHỦ TỊCH PHÓ CHỦ TỊCH Như Vàng 
	Output:``` {
    "personal_information": {
        "full_name": "đặng minh lai nam",
        "date_of_birth": {
            "numeric": "09/12/1984",
            "textual": "Ngày chín, tháng mười hai, năm một ngàn chín trăm tám mươi tư"
        },
        "gender": "Nam",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "place_of_birth": "Xã Phước Hải, huyện Long Đất, tỉnh Đồng Nai",
        "hometown": "" 
    },
    "mother_information": {
        "full_name": "Đặng THị MIÊN",
        "year_of_birth": "1965",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "residence": "Ấp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tinh Đồng Nai"
    },
    "father_information": {
        "full_name": "nguyễn văn hải",
        "year_of_birth": "1963",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "residence": "Áp Phước Thới, xã Phước Long Thọ, huyện Long Đất, tỉnh Đồng Nai"
    },
    "registration_information": {
        "registrar_name": "nhau",
        "registration_location": "Ủy ban nhân dân xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai",
        "registration_date": "26/5/1986"
    },
    "certificate_issuer": {
        "issued_by": "UBND HUYỆN ĐẤT ĐỎ",
        "issue_date": "09/06/2023",
        "document_number": "76/GKS-BS"
    }
} ```
"""

passport_schema = """
{
  "passport_number": "Unique identifier of the passport",
  "country_code": "ISO code of the issuing country",
  "full_name": "Passport holder's complete name",
  "nationality": "Passport holder's nationality",
  "date_of_birth": "Passport holder's birth date",
  "place_of_birth": "Passport holder's birthplace",
  "sex": "Passport holder's gender",
  "id_card_number": "Holder's national ID card number",
  "date_of_issue": "Date when the passport was issued",
  "date_of_expiry": "Date when the passport expires",
  "place_of_issue": "Location where the passport was issued"
}
"""
passport_examples = """

    Input: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM - SOCIALIST REPUBLIC OF VIETNAM PHỘ CHIẾU/PASSPORT Loại/Type Mã số /Code Số hộ chiếu / Passport N? P VNM N2449849 Họ và tên/Full name NGUYỄN HỮU CẦN Quốc tịch / Nationality VIẾT NAM /VIETNAMESE Ngày sinh/Date ofbirth Nơi sinh / Place of birth 01/01/1979 BA RIÁ - VÙNG TÀU Giới tính/Sex Số GCMND /ID card N3 NAMIM Ngày cấp/Date ofissue 19 Có giá trị đến 1 Date ofexpiry 1011/2021 1011/2022 Nơi cấp/Place ofissue Gia-oac-tay Jakarta IN 1990 THE IN ANNALIA UVENZZUINZPANERATION CONCERATION CONCECTIONALISTICALLY kkkko22 
    Output:``` {
        "passport_number": "N2449849",
        "country_code": "VNM",
        "full_name": "NGUYỄN HỮU CẦN",
        "nationality": "VIETNAMESE",
        "date_of_birth": "01/01/1979",
        "place_of_birth": "BA RIÁ - VÙNG TÀU",
        "sex": "M",
        "id_card_number": "",
        "date_of_issue": "10/11/2021",
        "date_of_expiry": "10/11/2022",
        "place_of_issue": "Gia-oac-tay Jakarta"
        } END

    Input: Mã sốyCode Sẽ hồ chiều TPassport Nam PHÓ CHIỀU PASSPORTS Loại/Type 02449798 P VNM Ho và tên V Full name Vothanh vu Quốc tích VNationality 1 VIRTNAM/VIETNAMESE Noav sinhVVDate of birth Nơi sinh IPlace of birth 0101/1987 KENGIANG Giới tính I Sex Số GCMND 1 ID cardM NAM/M Ngày cập/Date ofissue 19 Có giá trị đến / Date of expiry 204/11/2021 04711/2022 Nơi cấp/Place ofissue Gia-cac-ta V Jakarta 
    Output:``` {
        "passport_number": "02449798",
        "country_code": "VNM",
        "full_name": "Vothanh vu",
        "nationality": "VIETNAMESE",
        "date_of_birth": "01/01/1987",
        "place_of_birth": "KIENGIANG",
        "sex": "M",
        "id_card_number": "",
        "date_of_issue": "04/11/2021",
        "date_of_expiry": "04/11/2022",
        "place_of_issue": "Gia-cac-ta V Jakarta"
        } ```

    Input : PHÔ CHIỀU/PASSPORT Loai/Type Mã số/Code Số hộ chiếu /Passport N? N2449819 P VNM Ho và tên /Full name CAO HOANG NAM Quốc tịch / Nationality VIẾT NAM/VIETNAMESE Ngày sinh/Date ofbirth Nơi sinh /Place of birth 30/09/2001 KIENGIANGV 3 Giới tính/Sex Số GCMND/IDcard N ANAMIAM Ngày cấp /Date ofissue Có giá trị đến/Date ofexpiry 04/11/2021 04/11/2022 Nơi cấp / Place ofissue Gia-các-ta V Jakarta
    Output:``` {
        "passport_number": "N2449819",
        "passport_type": "P",
        "country_code": "VNM",
        "full_name": "CAO HOANG NAM",
        "nationality": "VIETNAMESE",
        "date_of_birth": "30/09/2001",
        "place_of_birth": "KIENGIANGV",
        "sex": "",
        "id_card_number": "",
        "date_of_issue": "04/11/2021",
        "date_of_expiry": "04/11/2022",
        "place_of_issue": "Gia-các-ta V Jakarta"
        } ```

"""
medical_schema = """
        {
        "current_institute": "name of the hospital or clinic issuing the prescription",
        "name": "patient full name",
        "gender": "patient's gender",
        "birth": "date of birth",
        "age": "patient's age",
        "address": "patient's address",
        "tel_customer": "patient phone number",
        "id_bhyt": "health insurance card number",
        "diagnosis": "diagnosis",
        "drugs": [{
            "drug_name": "drug name",
            "drug_dose": "drug dosage, usage and instructions",
            "drug_quantity": "drug quantity"
        }],
        "date_in": "issued date",
        "doctor_name": "doctor full name",
        }
        """
medical_examples = """
                Input: BỆNH VIỆN VIETT ĐỨC Số toa: 71 Nhà thuốc Bệnh viện Số điện thoại: 02435766328 Năm sinh: 1963 15A-Phương Mai-Đống Đa-Hà Nội PHIÊU THU TIỀN Xuất từ: Quầy Thuốc 1 In: Quầy Thuốc Lần in: 1 Giờ in: 08:15:54 Họ tên bệnh nhân: LÊ NGỌC LAN Mã bệnh nhân: 0029212798 Bác sĩ khám bệnh: Ths.BS TRỊNH MINH TRANG TT Tên mặt hàng ĐVT SL Đơn giá Thành tiền Spulit 100mg Viên 60 17.655 1.059.300 2 Ziaja Med Anti-imperfections Formula Cleansing Body Gel (Gel tắm ngừa khuẩn) 400ml Chai 1 499.460 499.460 3 Notis Antidanruff Shampoo 125ml Chai 2 248.600 497.200 4 Amisea 167mg Viên 30 6.420 192.600 5 Cafunten 10g Tuýp 4 6.527 26.108 Tổng khoản: 5 Tổng tiền: 2.274.668 Bằng chữ: Hai triệu hai trăm bảy mượi bốn nghìn sáu trăm sáu mươi tám đồng. Ngày 26 tháng 04 năm 2022 Người thu tiền Người nhận thuốc ngay trong ngày Lưu Trường hợp khách hàng có đơn tài chính đề nghị lấy (Quá ngày Bệnh viện không với nhân viên (Ký, họ tên) (Ký, họ tên) nhà thuốc để được hướng dẫn) Trân trọng cảm ơn Quý khách đã mua thuốc tại Bệnh viện. NGUYỄN HÀ MY LÊ NGỌC LAN
                Output:``` {
                    "current_institute": "BỆNH VIỆN VIỆT ĐỨC",
                    "name": "LÊ NGỌC LAN",
                    "gender": "",
                    "birth": "1963",
                    "age": "",
                    "address": "",
                    "tel_customer": "",
                    "id_bhyt": "",
                    "diagnosis": "",
                    "drugs": [
                        {
                            "drug_name": "Spulit 100mg",
                            "drug_dose": "",
                            "drug_quantity": "60 Viên"
                        },
                        {
                            "drug_name": "Ziaja Med Anti-imperfections Formula Cleansing Body Gel (Gel tắm ngừa khuẩn) 400ml",
                            "drug_dose": "",
                            "drug_quantity": "1 Chai"
                        },
                        {
                            "drug_name": "Notis Antidanruff Shampoo 125ml",
                            "drug_dose": "",
                            "drug_quantity": "2 Chai"
                        },
                        {
                            "drug_name": "Amisea 167mg",
                            "drug_dose": "",
                            "drug_quantity": "30 Viên"
                        },
                        {
                            "drug_name": "Cafunten 10g",
                            "drug_dose": "",
                            "drug_quantity": "4 Tuýp"
                        }
                    ],
                    "date_in": "Ngày 26 tháng 04 năm 2022",
                    "doctor_name": "Ths.BS TRỊNH MINH TRANG"
                } ```
           
                Input: ! Mã BN:2101002494 Số: 211002020 Mã hồ sơ: 2110150077 Kho:110-Kho Ngoại trú ĐƠN THUỐC BẢO HIỂM KKB.43333 Giới tính: Nam Đối tượng: Số thẻ BHYT: CK2383820079366 Địa chỉ: Lê Hoàn 2, Điện Biên, Thành phố Thanh Hóa, Tỉnh Thanh Hóa, Việt Nam Chẩn đoán: E11-Bệnh đái tháo đường không phụ thuộc insuline/ E78-1 Rối loạn chuyển Phòng: Phòng khám 326 Họ tên: LÊ HỒNG KHANH hóa lipoprotein và tình trạng tăng lipid máu khác / Bảo Hiểm Nơi ĐK KCB BĐ: 38280 Ngày sinh: 18/06/1956 Tuổi: 65 SĐT: 0912 660 254 STT Tên thuốc- Cách dùng ĐVT Số lượng BETICAPO 750 SR-750mg (Metformin) Ngày uống 1 viên sau ăn chiều. Viên 60 2 Gliclada 60mg modified- release tablets (Gliclazid) 3 Ngày uống 2 viên trước ăn sáng 30 phút TV. Fenofibrat- 200mg (Fenofibrat) Viên 120 Uống tối 1 viên ngay sau ăn Viên 60 Cộng khoản: 3 loại Lưu Khám lại khi thấy bất thường và khi hết thuốc. Kế toán Thủ kho Người bệnh Ngày 15 tháng 10 năm 2021 Bác sĩ khám (Ký và ghi rõ họ, tên) (Ký và ghi rõ họ, tên) Khih Lê Văn Chinh ISOFH-Người in: Lê Văn Chinh, ngày in: 15/10/2021 08:24
                Output:``` {
                    "current_institute": "",
                    "patient_name": "LÊ HỒNG KHANH",
                    "gender": "Nam",
                    "birth": "18/06/1956",
                    "age": "65",
                    "address": "Lê Hoàn 2, Điện Biên, Thành phố Thanh Hóa, Tỉnh Thanh Hóa, Việt Nam",
                    "tel_customer": "0912 660 254",
                    "id_bhyt": "CK2383820079366",
                    "diagnosis": "E11 - Bệnh đái tháo đường không phụ thuộc insuline / E78 - Rối loạn chuyển hóa lipoprotein và tình trạng tăng lipid máu khác",
                    "drugs": [
                        {
                            "drug_name": "BETICAPO 750 SR-750mg (Metformin)",
                            "drug_dose": "Ngày uống 1 viên sau ăn chiều",
                            "drug_quantity": "60 Viên"
                        },
                        {
                            "drug_name": "Gliclada 60mg modified-release tablets (Gliclazid)",
                            "drug_dose": "Ngày uống 2 viên trước ăn sáng 30 phút",
                            "drug_quantity": "120 viên"
                        },
                        {
                            "drug_name": "Fenofibrat-200mg (Fenofibrat)",
                            "drug_dose": "Uống tối 1 viên ngay sau ăn",
                            "drug_quantity": "60 viên"
                        }
                    ],
                    "date_in": "Ngày 15 tháng 10 năm 2021",
                    "doctor_name": "Lê Văn Chinh"
                } ```
           
                Input: Tp.HCM Xem tóm tăt bệnh án Bệnh viện Da Liễu ĐT: (028) 39308131 Mã BN: 22368078 P.khám 7 ĐƠN THUỐC ĐT: 0965839049 Họ và tên: TRỊNH PHẠM KIỀU NGA. 18 tháng. Nữ Địa chỉ: ,,Xã Tân Tây,Huyện Gò Công Đông,Tỉnh Tiền Giang Chẩn đoán: (L70;) Trứng cá; Thuốc điều trị: 1 Minocyclin 50mg (Zalenka) 30 Viên Uống, sáng 1 viên, chiều 1 viên 2 L-Cystin 500mg (Elovess) 30 Viên Uống, sáng 1 viên, chiều l viên 3 Cetirizin (10mg) (Cetimed) 15 Viên Uống,, chiều 1 viên 4 Lưu huỳnh 5% (Cream Lưu Huỳnh) 2 Lọ Bôi., sáng 1 lần, tối 1 lần thân cộng:4 khoản Ngày cấp đơn 07 tháng 12 năm 2022 - Tái khám: 1 Bác sĩ điều trị + Khi hết thuốc uống hoặc + Bệnh nặng hơn Bs.CKII Hồ Thị Mỹ Châu BENH VIỆN DA LIEU KHU KHÁM THEO YÊU lọc dinh dưỡng: CN: 53Kg; CC: 156 Cm ;BMI: 21 Kg/m2 ên người đưa trẻ đến khám: Khuyến cáo dinh dưỡng: -Ăn đầy đủ chất dinh dưỡng, đặc biệt vitamin A, C,E, kẽm, omega 3... Hạn chế uống sữa, thức ăn nhiều tinh bột, nhiều đường, nhiều dầu mỡ, tránh căng thẳng. hám lại xin mang theo đơn này Tờ:[1-2]
                Output:``` {
                        "current_institute": "Bệnh viện Da Liễu",
                        "patient_name": "TRỊNH PHẠM KIỀU NGA",
                        "gender": "Nữ",
                        "birth": "",
                        "age": "18 tháng",
                        "address": "Xã Tân Tây, Huyện Gò Công Đông,Tỉnh Tiền Giang",
                        "tel_customer": "0965839049",
                        "id_bhyt": "",
                        "diagnosis": "(L70;) Trứng cá;",
                        "drugs": [
                            {
                                "drug_name": "Minocyclin 50mg (Zalenka)",
                                "drug_dose": "sáng 1 viên, chiều 1 viên",
                                "drug_quantity": "30 viên"
                            },
                            {
                                "drug_name": "L-Cystin 500mg (Elovess)",
                                "drug_dose": "sáng 1 viên, chiều 1 viên",
                                "drug_quantity": "30 viên"
                            },
                            {
                                "drug_name": "Cetirizin (10mg) (Cetimed)",
                                "drug_dose": "chiều 1 viên",
                                "drug_quantity": "15 viên"
                            },
                            {
                                "drug_name": "Lưu huỳnh 5% (Cream Lưu Huỳnh)",
                                "drug_dose": "bôi sáng 1 lần, tối 1 lần",
                                "drug_quantity": "2 lọ"
                            }
                        ],
                        "date_in": "07 tháng 12 năm 2022",
                        "doctor_name": "Bs.CKII Hồ Thị Mỹ Châu"
                    } ```   
                    """
invoices_schema = """
                    {
                        "shop_name": "The name of the shop or store where the purchase was made",
                        "cashier_name": "Name of the cashier who processed the transaction",
                        "price_total": "The total price of all items before any discounts are applied",
                        "price_discount": "The total amount of discount applied to the purchase",
                        "price_unpaid": "The amount that remains unpaid after the transaction, if any",
                        "customer_name": "Name of the customer making the purchase",
                        "price_final": "The final price to be paid by the customer after discounts and additions",
                        "cashier_id": "Unique identifier for the cashier responsible for the transaction",
                        "customer_phone_number": "Phone number of the customer",
                        "price_total_paid": "The total amount paid by the customer, including any unpaid balance from previous transactions"
                    }
                """
invoices_examples = """

                        Input: THE COFFEE HOUSE
                            36 Hoàng Cầu, P.Ô Chợ Dừa, Q.Đống Đa, Hà Nội
                            Số 17
                            Thời gian:
                            30.06.2023003.33
                            Thu ngân:
                            CASH1
                            Số Bill:
                            122406017252023
                            Khách hàng:
                            TT
                            Tên món
                            SL
                            Đ.Giá
                            T.Tiên
                            Cold Brew Phúc
                            1 Bon Tử (Lớn)
                            1
                            55000
                            55 000
                            2
                            Nguội
                            Bánh MiVN Thịt
                            1
                            35000
                            35 000
                            Tổng số lượng:
                            2
                            Thành tien!
                            90000
                            + Giảm giá:
                            16 000
                            Thanh Toán ;
                            74000
                            Tiên khách đưa:
                            74000
                            Tiền thừa:
                            0
                            + The Visa
                            74000
                            Giá sản phẩm đã bao gồm thuế VAT 10%.
                            Phiêu này chỉ có giá trị xuất hóa đon trong
                            vòng 2 tiếng từ khi hoàn tất mua hàng.
                            Hãy quét QR code phía trên hoặc truy cập Q
                            websizehttpss/teeeeeeee...
                            Mọi thắc mắc xin liên hệ 02871 087 088
                            Password Wifi:
                            thecoffeehouse
                        Output:``` {
                            "shop_name": "THE COFFEE HOUSE, 36 Hoàng Cầu, P.Ô Chợ Dừa, Q.Đống Đa, Hà Nội",
                            "cashier_name": "CASH1",
                            "price_total": "90000", // Total price before discount
                            "price_discount": "16000", // Discount applied
                            "price_unpaid": "0", // Assuming the whole amount is paid as no unpaid amount is mentioned
                            "customer_name": "TT", // Customer name abbreviation
                            "price_final": "74000", // Final price after discount
                            "cashier_id": "122406017252023", // Assuming the 'Số Bill' is the cashier ID
                            "customer_phone_number": "", // Customer phone number is not provided
                            "price_total_paid": "74000" // Total amount paid by the customer
                        } ```

                        Input: CIRCLE R
                            Store:HN2180
                            Lo 7, khu di dan Den Lu 2, Phuong Hoang Va
                            n Thu, Quan Hoang Mai, Thanh Pho Ha Nai,V
                            iet Nam
                            Receipt:RW
                            Date :Wed
                            05 Jul 2023 21:31:00
                            Terminal:01
                            CashierName:Nguyen
                            Thị Phuong Anh
                            ITEM UnitPrice Qty
                            Amount
                            UIU II II - II
                            SATORI NUOO Tinh Khiet 1.5L/1 Ch 12,000
                            DASANI NUOC Suoi Tinh Khiet 1.5L 13,000
                            SOMERSBY NUOC Tao Len Men Vi Tao 23,000
                            AOKI Com Nam Cuon Ga Sot Terriya 24,000
                            G Cha Lua Que Bi 50g/1 Goi
                            14,000
                            (LB/58793) Coupon-Cash 10k cho -10,000
                            (LB/58792) Mua hd tu 40k tang coupon -1
                            Total Item(s) Qty:
                            5
                            Subtotal:
                            86,000 VND
                            Total Discount
                            --100011 VND
                            Total(+VAT):
                            75,999VND
                            Card:
                            75,999 VND
                            VISA
                            --Card Number:
                            4**********
                            -RReferneedd 000601000671
                            -Holder:
                            *************************
                            --ApprCoder 267414
                            - TranID:
                            000462
                            CHANGE W an Tn
                            IN DUE:
                            NES
                            0 VND
                            1 Item(s)

                        Output:``` {
                                "shop_name": "CIRCLE R, Store:HN2180, Lo 7, khu di dan Den Lu 2, Phuong Hoang Van Thu, Quan Hoang Mai, Thanh Pho Ha Nai, Viet Nam",
                                "cashier_name": "Nguyen Thị Phuong Anh",
                                "price_total": "86000", // Subtotal before discounts
                                "price_discount": "10001", // Total discount applied
                                "price_unpaid": "0", // Assuming the whole amount is paid as no unpaid amount is mentioned
                                "customer_name": "", // Customer name is not provided
                                "price_final": "75999", // Final price after discount and VAT
                                "cashier_id": "Receipt:RW, Date: Wed 05 Jul 2023 21:31:00, Terminal:01", // Including receipt, date, and terminal as identifier
                                "customer_phone_number": "", // Customer phone number is not provided
                                "price_total_paid": "75999" // Total amount paid by the customer
                            } ```
"""
template_kie = """
                You are an AI Assistant in general field. Your goal is to provide the extracted information from the input. Think step by step and never skip any step.
                Please try to extract all data points and correct  errors based on the description of the data points, especially those related to dates . Do not add or omit any information. If you don't know, just answer "don't know" and do not include information that is not in the document in your answer.
                {schema}
               
                EXAMPLES
                ----
                {examples}
                ------    
                Input: {content}
                Output:```
    """.strip()

template_general = """ You are an hepful AI assistant, your goal is provide a short helpful respone about the problem that User asked below.
                The user's input will always start with "User:" and don't have any end character constraint. 
                The AI asssistant's response will always start with "AI assistant:" and don't have any end character constraint.
                Example:
                ----
                User: Who was Picasso's wife ? \n AI assistant: Olga Koklova.
                User: Tell me about Donald Trump \n AI assistant : Donald Trump is 44th president of United States of American.
                ----
                User: {content} \n AI asssitant:
                """