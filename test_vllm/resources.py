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
	Human: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc thái Số: 158 GIẤY KHAI SINH (BÁN SAO) Họ, chữ đệm, tên: huỳnh thị tú trinh Ngày, tháng, năm sinh: 01/01/1990 - ghi bằng chữ: Ngày một, tháng một, năm một ngàn chín trăm chín mươi - Giới tính: Nữa Dân tộc: Kinh Quốc tịch: Việt Nam Nơi sinh: Bảo sanh Long Đất, tỉnh Bà Rịa - Vũng Tàu Quê quán: Số định danh cá nhân: Họ, chữ đệm, tên người mẹ: bùi THị TỐT Năm sinh: 1968 Dân tộc: Kinh Quốc tịch: Việt Nam Xã Nơi cư trú: Áp Thanh Long, xã Phước Thạnh, huyện Long Đất, tỉnh Bà Rịa ? Vũng Tàu Nhà Nhau Họ, chữ đệm, tên người cha: huỳnh văn sa Năm sinh: 1967 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Áp. Tường Thành, xã Phước Long Thọ, huyện Long Đất, tỉnh Bà Rịa ? Vũng Tàu Họ, chữ đệm, tên người đi khai sinh: Giấy tờ tùy thân: Nơi đăng ký khai sinh: Ủy ban nhân dân xã Phước Long Thọ, huyện Long Đất, tỉnh Bà Rịa Nhà Nhà Nhiều Vũng Tàu Ngày, tháng, năm đăng ký: 19/8/1996 NGƯỜI KÝ GIÁY KHAI SINH (Đã ký) Sao từ Sổ đăng ký khai sinh TỈNH BÀ RỊA - VŨNG TÀU Đất Đỏ, ngày 0 9 tháng 6 năm 2023 HUBND HUYỆN ĐẤT ĐỎ NGƯỜI KÝ Thuật (Ký, ghi rõ họ, tên, chức vụ và đóng dấu) Số: 69/GKS-BS KT. CHỦ TỊCH PHÓ CHỦ TỊCH BÊN ĐÁ Bằng Như Vàng Trị 
	AI ASSISTANT:{
    "personal_information": {
        "full_name": "huỳnh thị tú trinh",
        "date_of_birth": {
            "numeric": "01/01/1990",
            "textual": "Ngày một, tháng một, năm một ngàn chín trăm chín mươi"
        },
        "gender": "Nữa",  
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
} END

	Human: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc Số: 390 GIẤY KHAI SINH (BẢN SAO) Họ, chữ đệm, tên: NGUYỄN VĂN LỢI Ngày, tháng, năm sinh: 02/7/1990 - ghi bằng chữ: Ngày hai, tháng bảy, năm một ngàn chín trăm chín mươi Giới tính: Nam Dân tộc: Kinh Quốc tịch: Việt Nam Nơi sinh: Trạm xá Phước Hải, huyện Long Đất, tỉnh Đồng Nai Quê quán Số định danh cá nhân: Họ, chữ đệm, tên người mẹ: PHAN THỊ Được Năm sinh: 1963 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Áp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Họ, chữ đệm, tên người cha: nguyễn qua Năm sinh: 1959 - Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Ấp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Họ, chữ đệm, tên người đi khai sinh: Giấy tờ tùy thân: Thuật Nơi đăng ký khai sinh: Ủy ban nhân dân xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Nhân Thuận Ngày, tháng, năm đăng ký: 07/8/1990 NGƯỜI KÝ GIẤY KHAI SINH (Đã ký) Sao từ Sổ đăng ký khai sinh TỈNH BÀ RỊA - VŨNG TÀU Đất Đỏ, ngày 09 tháng 6 năm 2023 UBND HUYỆN ĐẤT ĐỎ NGƯỜI KÝ (Kỷ, ghi rõ họ, tên, chức vụ và đóng dấu) Số: 20/GKS-BS KT. CHỦ TỊCH PHÓ CHỦ TỊCH VIỆN ĐA Như Vàng 
	AI ASSISTANT: {
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
} END
	Human: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc Số: 178 GIẤY KHAI SINH (BÁN SAO) Xã Họ, chữ đệm, tên: đặng minh lai nam Ngày, tháng, năm sinh: 09/12/1984 - ghi bằng chữ: Ngày chín, tháng mười hai, năm một ngàn chín trăm tám mươi tư này Giới tính: Nam Dân tộc: Kinh Quốc tịch: Việt Nam Xã Nơi sinh: Xã Phước Hải, huyện Long Đất, tỉnh Đồng Nai Nam Quê quán: Số định danh cá nhân: Họ, chữ đệm, tên người mẹ: Đặng THị MIÊN Năm sinh: 1965 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Ấp Hội Mỹ, xã Phước Long Hội, huyện Long Đất, tinh Đồng Nai Họ, chữ đệm, tên người cha: nguyễn văn hải Năm sinh: 1963 Dân tộc: Kinh Quốc tịch: Việt Nam Nơi cư trú: Áp Phước Thới, xã Phước Long Thọ, huyện Long Đất, tỉnh Đồng Nai Xã Họ, chữ đệm, tên người đi khai sinh: nhau Giấy tờ tùy thân: Nơi đăng ký khai sinh: Ủy ban nhân dân xã Phước Long Hội, huyện Long Đất, tỉnh Đồng Nai Ngày, tháng, năm đăng ký: 26/5/1986 NGƯỜI KÝ GIẤY KHAI SINH (Đã ký) TỈNH BÀ RỊA - VŨNG TÀU Sao từ Sổ đăng ký khai sinh 19 Đất Đỏ, ngày 09 tháng 6 năm 2023 UBND HUYỆN ĐẤT ĐỎ NGƯỜI KÝ (Ký, ghi rõ họ, tên, chức vụ và đóng dấu) Số: 76/GKS-BS KT.CHỦ TỊCH PHÓ CHỦ TỊCH Như Vàng 
	AI ASSISTANT: {
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
        "hometown": "" s
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
} END
"""

schema_passport = """
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
examples_passport = """

            Human: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM - SOCIALIST REPUBLIC OF VIETNAM PHỘ CHIẾU/PASSPORT Loại/Type Mã số /Code Số hộ chiếu / Passport N? P VNM N2449849 Họ và tên/Full name NGUYỄN HỮU CẦN Quốc tịch / Nationality VIẾT NAM /VIETNAMESE Ngày sinh/Date ofbirth Nơi sinh / Place of birth 01/01/1979 BA RIÁ - VÙNG TÀU Giới tính/Sex Số GCMND /ID card N3 NAMIM Ngày cấp/Date ofissue 19 Có giá trị đến 1 Date ofexpiry 1011/2021 1011/2022 Nơi cấp/Place ofissue Gia-oac-tay Jakarta IN 1990 THE IN ANNALIA UVENZZUINZPANERATION CONCERATION CONCECTIONALISTICALLY kkkko22 
            AI ASSISTANT:{
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

            Human: Mã sốyCode Sẽ hồ chiều TPassport Nam PHÓ CHIỀU PASSPORTS Loại/Type 02449798 P VNM Ho và tên V Full name Vothanh vu Quốc tích VNationality 1 VIRTNAM/VIETNAMESE Noav sinhVVDate of birth Nơi sinh IPlace of birth 0101/1987 KENGIANG Giới tính I Sex Số GCMND 1 ID cardM NAM/M Ngày cập/Date ofissue 19 Có giá trị đến / Date of expiry 204/11/2021 04711/2022 Nơi cấp/Place ofissue Gia-cac-ta V Jakarta 
            AI ASSISTANT:{
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
        }END

            Human : PHÔ CHIỀU/PASSPORT Loai/Type Mã số/Code Số hộ chiếu /Passport N? N2449819 P VNM Ho và tên /Full name CAO HOANG NAM Quốc tịch / Nationality VIẾT NAM/VIETNAMESE Ngày sinh/Date ofbirth Nơi sinh /Place of birth 30/09/2001 KIENGIANGV 3 Giới tính/Sex Số GCMND/IDcard N ANAMIAM Ngày cấp /Date ofissue Có giá trị đến/Date ofexpiry 04/11/2021 04/11/2022 Nơi cấp / Place ofissue Gia-các-ta V Jakarta
            AI ASSISTANT:{
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
        } END

"""