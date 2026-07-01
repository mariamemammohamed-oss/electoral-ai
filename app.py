import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="المساعد الانتخابي الذكي", layout="centered")

# عرض صورة المساعد الترحيبية
st.image("robot.png", width=200)

st.title("🤖 المساعد الانتخابي الذكي")

# زرار تشغيل الصوت الترحيبي الذكي
if st.button("🔊 اضغط هنا لسماع التعليمات الصوتية"):
    file_option_1 = "voice.mp3"
    file_option_2 = "voice.mp3.mp3"
    
    selected_file = None
    if os.path.exists(file_option_1):
        selected_file = file_option_1
    elif os.path.exists(file_option_2):
        selected_file = file_option_2
        
    if selected_file:
        with open(selected_file, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    else:
        st.error("برجاء التأكد من وضع ملف الصوت في نفس المجلد الموجود به هذا الكود (app.py).")

st.markdown("---")

# مصفوفة تشمل الاسم المرفوع على جيت هوب بالظبط بحروف كبيرة بالكامل لضمان التشغيل المباشر
excel_options = [
    "DATA.xlsx",
    "Data.xlsx", 
    "data.xlsx", 
    "DATA.xlsx.xlsx",
    os.path.join(os.getcwd(), "DATA.xlsx")
]

selected_excel = None
for option in excel_options:
    if os.path.exists(option):
        selected_excel = option
        break

# قراءة كل الشيتات من ملف الإكسيل المتاح
if selected_excel:
    try:
        # قراءة ملف الإكسيل بجميع الشيتات
        xls = pd.ExcelFile(selected_excel)
        
        # اختيار الصفحة
        st.subheader("📋 القوائم المتاحة:")
        sheet = st.selectbox("اضغط هنا للاختيار بين الناخبين والمرشحين:", xls.sheet_names)
        df = pd.read_excel(selected_excel, sheet_name=sheet)
        
        # معرفة ترتيب الشيت الحالي
        all_sheets = list(xls.sheet_names)
        current_index = all_sheets.index(sheet)
        
        # --- الفصل التام والنهائي بين الشيتات ---
        
        # إذا اختار الشيت الثاني (أسماء المرشحين) -> يعرض الجدول فوراً للاطلاع
        if current_index > 0:
            st.markdown("---")
            st.header(f"👥 كشف أسماء المرشحين - {sheet}")
            st.info("إليك جدول بأسماء المرشحين للاطلاع المباشر:")
            st.dataframe(df, use_container_width=True)
            
        # إذا اختار الشيت الأول (الخاص بالناخبين والبحث)
        else:
            st.markdown("---")
            st.header("🔍 الاستعلام عن المركز الانتخابي")
            number = st.text_input("📝 أدخل الرقم التعريفي الخاص بك:")
            
            if st.button("🔍 بدء البحث"):
                if number:
                    number = str(number).strip()
                    result = df[df.iloc[:, 0].astype(str).str.strip() == number]
                    
                    if not result.empty:
                        st.success("تم العثور على بياناتك بنجاح ✔️")
                        st.dataframe(result)
                        
                        # --- عنصر الـ QR Code التفاعلي للخريطة ---
                        st.markdown("---")
                        st.subheader("📍 الخريطة الانتخابية والوصول للمركز")
                        
                        map_url = "https://www.arcgis.com/apps/instant/nearby/index.html?appid=565a2a9c65624173ad93ccf419041ff5&sliderDistance=5"
                        # توليد كود QR مباشر وآمن من الإنترنت تماماً
                        online_qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={map_url}"
                        
                        st.markdown(
                            f"""
                            <div style="text-align: center; margin-top: 10px;">
                                <a href="{map_url}" target="_blank">
                                    <img src="{online_qr}" alt="QR Code الخريطة" style="width: 150px; border: 3px solid #FF4B4B; padding: 5px; border-radius: 10px; cursor: pointer;">
                                </a>
                                <p style="color: gray; font-size: 14px; margin-top: 8px; font-weight: bold;">(اضغطي على صورة الـ QR Code المربع فوق لتفتح الخريطة التفاعلية فوراً)</p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    else:
                        st.error("الرقم التعريفي غير موجود في هذا الشيت ❌")
                else:
                    st.warning("برجاء إدخال الرقم التعريفي أولاً.")
                    
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة البيانات: {e}.")
else:
    st.error("❌ ملف البيانات غير موجود. تأكدي من أن الملف مرفوع بنجاح على جيت هوب.")