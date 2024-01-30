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

business_registration_schema = """
{
            "city": "The city where the business is registered",
            "certificate_type": "The type of document issued for business registration",
            "business_registration_number": "Unique identifier of the business registration",
            "first_registration_date": "The date when the business was first registered",
            "latest_registration_amendment": {
                "amendment_number": "The number indicating how many times the registration has been amended",
                "date": "The date of the latest registration amendment"
            },
            "company_name": {
                "in_vietnamese": "The official name of the company in Vietnamese",
                "in_foreign_language": "The official name of the company in a foreign language, if applicable",
                "abbreviated": "The abbreviated name of the company"
            },
            "head_office_address": "The physical address of the company's head office",
            "contact_information": {
                "telephone": "The telephone number of the company",
                "fax": "The fax number of the company",
                "email": "The email address of the company",
                "website": "The official website of the company"
            },
            "charter_capital": {
                "amount": "The total amount of the company's charter capital",
                "in_words": "The total amount of the charter capital written out in words",
                "share_nominal_value": "The nominal value of each share in the company"
            },
            "legal_representative": {
                "full_name": "The full name of the company's legal representative",
                "gender": "The gender of the legal representative",
                "position": "The official position of the legal representative within the company",
                "date_of_birth": "The birth date of the legal representative",
                "ethnicity": "The ethnicity of the legal representative",
                "nationality": "The nationality of the legal representative",
                "personal_identification_document": {
                    "type": "The type of personal identification document",
                    "number": "The number of the identification document",
                    "date_of_issue": "The issue date of the identification document",
                    "place_of_issue": "The place where the identification document was issued"
                },
                "permanent_residence": "The permanent residence address of the legal representative",
                "current_residence": "The current residence address of the legal representative"
            },
            "registration_officer": "The name of the officer who processed the business registration"
        }
"""

business_registration_examples = """

                                        Input:SỞ KẾ HOẠCH VÀ ĐẦU TƯ
                                        CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
                                        THÀNH PHỐ HỒ CHÍ MINH
                                        Độc lập
                                        - Tự do - Hạnh phúc
                                        PHÒNG ĐĂNG KÝ KINH DOANH
                                        GIẤY CHỨNG NHẬN ĐĂNG KÝ DOANH NGHIỆP
                                        CÔNG TY CỔ PHẦN
                                        Mã số doanh nghiệp:
                                        0309829579
                                        Đăng ký lần đầu:
                                        ngày 11 tháng 03 năm 2010
                                        Đăng ký thay đổi lần thứ:
                                        7, ngày 29 tháng 11 năm 2017
                                        1. Tên công ty
                                        Tên công ty viết bằng tiếng Việt:
                                        CÔNG TY CỔ PHẦN TRUNG TÂM CHĂM SÓC
                                        SỨC KHÓE CỘNG ĐỒNG CHAC
                                        Tên công ty viết bằng tiếng nước ngoài:
                                        CHAC COMMUNITY HEALTHCARE
                                        CENTER CORPORATION
                                        Tên công ty viết tắt:
                                        TRUNG TÂM CHĂM SÓC SỨC KHỎE CỘNG ĐÔNG CHAC
                                        2. Địa chỉ trụ sở chính
                                        110A Ngô Quyền, Phường 08, Quận 5, Thành phố Hồ Chí Minh, Việt Nam
                                        Điện thoại:
                                        0902714743
                                        Fax:
                                        Email:
                                        Website:
                                        3. Vốn điều lệ
                                        Vốn điều lệ:
                                        8.000.000.000 đồng
                                        Bằng chữ:
                                        Tám tỷ đồng
                                        Mệnh giá cổ phần:
                                        10.000 đồng
                                        Tổng số cổ phần:
                                        4. Người đại diện theo pháp luật của công ty
                                        * Họ và tên:
                                        NGÔ HỚN ĐÌNH
                                        Giới tính:
                                        Nam
                                        Chức danh:
                                        Giám đốc
                                        Sinh ngày:
                                        25/07/1984
                                        Dân tộc:
                                        Hoa
                                        Quốc tịch:
                                        Việt Nam
                                        Loại giấy tờ chứng thực cá nhân:
                                        Chứng minh nhân dân
                                        Số giấy chứng thực cá nhân:
                                        023692354
                                        Ngày cấp:
                                        23/06/2005
                                        Nơi cấp:
                                        Công an Thành phố Hồ Chí Minh
                                        Nơi đăng ký hộ khẩu thường trú:
                                        1442/46 đường 3/2, Phường 2. Quận 11. Thành phố
                                        Hồ Chí Minh, Việt Nam
                                        Chỗ ở hiện tại:
                                        1442/46 đường 3/2, Phường 2, Quận 11, Thành phố Hồ Chí Minh,
                                        Việt Nam
                                        W/TRỞNNG PHÒNGôôg
                                        HOACH A
                                        PHÒNG
                                        ĐĂNG KY
                                        KINH DOANH
                                        NAPPHHG II     AA
                                        Hồ Hoành Sơn
                                        Output:``` {
                        "city": "Thành phố Hồ Chí Minh",
                        "certificate_type": "GIẤY CHỨNG NHẬN ĐĂNG KÝ DOANH NGHIỆP",
                        "business_registration_number": "0309829579",
                        "first_registration_date": "ngày 11 tháng 03 năm 2010",
                        "latest_registration_amendment": {
                            "amendment_number": "7",
                            "date": "ngày 29 tháng 11 năm 2017"
                        },
                        "company_name": {
                            "in_vietnamese": "CÔNG TY CỔ PHẦN TRUNG TÂM CHĂM SÓC SỨC KHÓE CỘNG ĐỒNG CHAC",
                            "in_foreign_language": "CHAC COMMUNITY HEALTHCARE CENTER CORPORATION",
                            "abbreviated": "TRUNG TÂM CHĂM SÓC SỨC KHỎE CỘNG ĐÔNG CHAC"
                        },
                        "head_office_address": "110A Ngô Quyền, Phường 08, Quận 5, Thành phố Hồ Chí Minh, Việt Nam",
                        "contact_information": {
                            "telephone": "0902714743",
                            "fax": "",
                            "email": "",
                            "website": ""
                        },
                        "charter_capital": {
                            "amount": "8.000.000.000 đồng",
                            "in_words": "Tám tỷ đồng",
                            "share_nominal_value": "10.000 đồng"
                        },
                        "legal_representative": {
                            "full_name": "NGÔ HỚN ĐÌNH",
                            "gender": "Nam",
                            "position": "Giám đốc",
                            "date_of_birth": "25/07/1984",
                            "ethnicity": "Hoa",
                            "nationality": "Việt Nam",
                            "personal_identification_document": {
                                "type": "Chứng minh nhân dân",
                                "number": "023692354",
                                "date_of_issue": "23/06/2005",
                                "place_of_issue": "Công an Thành phố Hồ Chí Minh"
                            },
                            "permanent_residence": "1442/46 đường 3/2, Phường 2, Quận 11, Thành phố Hồ Chí Minh, Việt Nam",
                            "current_residence": "1442/46 đường 3/2, Phường 2, Quận 11, Thành phố Hồ Chí Minh, Việt Nam"
                        },
                        "registration_officer": "Hồ Hoành Sơn"
                    } ```

                                    Input: SỞ KẾ HOẠCH VÀ ĐẦU TƯ
                                    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
                                    THÀNH PHỐ HỒ CHÍ MINH
                                    Độc lập - Tự do X Hạnh phúc
                                    PHÒNG ĐĂNG KÝ KINH DOANH
                                    GIẤY CHỨNG NHẬN ĐĂNG KÝ DOANH NGHIỆP
                                    CÔNG TY CỔ PHẦN
                                    Mã số doanh nghiệp:
                                    0301442227
                                    Đăng ký lần đầu:
                                    ngày 17 tháng 02 năm 2005
                                    Đăng ký thay đổi lần thứ:
                                    8, ngày 03 tháng 01 năm 2018
                                    1. Tên công ty
                                    Tên công ty viết bằng tiếng Việt:
                                    CÔNG TY CỔ PHÂN ĐẦU TƯ VÀ PHÁT TRIỂN
                                    XÂY DỰNG
                                    Tên công ty viết bằng tiếng nước ngoài:
                                    INVESTMENT & CONSTRUCTION
                                    DEVELOPMENT CORPORATION
                                    Tên công ty viết tắt:
                                    INVESTCO. CORP
                                    2. Địa chỉ trụ sở chính
                                    201 Võ Thị Sáu, Phường 07, Quận 3, Thành phố Hồ Chí Minh, Việt Nam
                                    Điện thoại:
                                    08.9320678
                                    Fax:
                                    08.9320679
                                    Email:
                                    invesco@@nvescovv..om
                                    Websiter www.invesco.com.vn
                                    3. Vốn điều lệ
                                    Vốn điều lệ:
                                    208.097.020.000 đồng
                                    Bằng chữ:
                                    Hai trăm lẻ tám tỷ không trăm chín mươi bảy triệu không
                                    trăm hai mươi nghìn đồng
                                    Mệnh giá cổ phần:
                                    100.000 đồng
                                    Tổng số cổ phần:
                                    4. Người đại diện theo pháp luật của công ty
                                    * Họ và tên:
                                    NGUYỄN DUY HƯNG
                                    Giới tính:
                                    Nam
                                    Chức danh:
                                    Tổng giám đốc
                                    Sinh ngày:
                                    24/03/1981
                                    Dân tộc:
                                    Kinh
                                    Quốc tịch:
                                    Việt Nam
                                    Loại giấy tờ chứng thực cá nhân:
                                    Chứng minh nhân dân
                                    Số giấy chứng thực cá nhân:
                                    011958158
                                    Ngày cấp:
                                    17/05/2006
                                    Nơi cấp:
                                    Công an Thành phố Hà Nội
                                    Nơi đăng ký hộ khẩu thường trú:
                                    Số 56, Tổ 8, Phường Ngọc Hà, Quận Ba Đình,
                                    Thành phố Hà Nội, Việt Nam
                                    Chỗ Ở hiện tại:
                                    Số 201, đường Võ Thị Sáu, Phường 07, Quận 3, Thành phố Hồ Chí
                                    Minh, Việt Nam
                                    AEERR PHÒNG
                                    PHÒNG nhn Trưởng Phòng
                                    ĐĂNG KÝ
                                    KINH
                                    www.LLA
                                    Võ Thành Thơ
                                    Output:```  {
    "city": "Thành phố Hồ Chí Minh",
    "certificate_type": "GIẤY CHỨNG NHẬN ĐĂNG KÝ DOANH NGHIỆP",
    "business_registration_number": "0301442227",
    "first_registration_date": "ngày 17 tháng 02 năm 2005",
    "latest_registration_amendment": {
        "amendment_number": "8",
        "date": "ngày 03 tháng 01 năm 2018"
    },
    "company_name": {
        "in_vietnamese": "CÔNG TY CỔ PHÂN ĐẦU TƯ VÀ PHÁT TRIỂN XÂY DỰNG",
        "in_foreign_language": "INVESTMENT & CONSTRUCTION DEVELOPMENT CORPORATION",
        "abbreviated": "INVESTCO. CORP"
    },
    "head_office_address": "201 Võ Thị Sáu, Phường 07, Quận 3, Thành phố Hồ Chí Minh, Việt Nam",
    "contact_information": {
        "telephone": "08.9320678",
        "fax": "08.9320679",
        "email": "invesco@@nvescovv..om",
        "website": "www.invesco.com.vn"
    },
    "charter_capital": {
        "amount": "208.097.020.000 đồng",
        "in_words": "Hai trăm lẻ tám tỷ không trăm chín mươi bảy triệu không trăm hai mươi nghìn đồng",
        "share_nominal_value": "100.000 đồng"
    },
    "legal_representative": {
        "full_name": "NGUYỄN DUY HƯNG",
        "gender": "Nam",
        "position": "Tổng giám đốc",
        "date_of_birth": "24/03/1981",
        "ethnicity": "Kinh",
        "nationality": "Việt Nam",
        "personal_identification_document": {
            "type": "Chứng minh nhân dân",
            "number": "011958158",
            "date_of_issue": "17/05/2006",
            "place_of_issue": "Công an Thành phố Hà Nội"
        },
        "permanent_residence": "Số 56, Tổ 8, Phường Ngọc Hà, Quận Ba Đình, Thành phố Hà Nội, Việt Nam",
        "current_residence": "Số 201, đường Võ Thị Sáu, Phường 07, Quận 3, Thành phố Hồ Chí Minh, Việt Nam"
    },
    "registration_officer": "Võ Thành Thơ"
} ```
"""