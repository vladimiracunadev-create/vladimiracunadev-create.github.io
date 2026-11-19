#!/usr/bin/env python3
"""Publish the "Consulta inhabilidades para trabajar con menores de edad" PDF.

The Spanish PDF is the official document issued by the Servicio de Registro
Civil e Identificacion de Chile and is copied **without alteration**. The other
21 locale variants are courtesy translations that carry the facts read from
that source PDF (RUN, name, date, result) plus a banner stating that only the
Spanish original is official.

Usage:
    python scripts/generate-consulta-inhabilidades.py \
        --source C:/dev/agente-laboral-claude/perfil/cv/Consulta_inhabilidades.pdf
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
TMP = ROOT / "tmp" / "pdfs"
CONTRACT = json.loads((ROOT / "data" / "portfolio-i18n.json").read_text(encoding="utf-8"))
BASE_NAME = "consulta-inhabilidades"
PUBLIC_URL = "https://vladimiracunadev-create.github.io/assets/consulta-inhabilidades.pdf"
DEFAULT_SOURCE = Path(r"C:\dev\agente-laboral-claude\perfil\cv\Consulta_inhabilidades.pdf")

# title, greeting, intro, "RUN", "NAME", result, "date", reminder, warning, banner
T = {
    "en": ["Inquiry on disqualifications to work with minors", "Dear user:",
           "The Civil Registry and Identification Service (Servicio de Registro Civil e Identificación) reports that Mr./Ms.:",
           "RUN", "NAME", "DOES NOT have any disqualifications to work with minors.", "Date",
           "We remind you that you may make this inquiry if you need to hire the person for a job or position involving direct and regular contact with minors, or similar purposes.",
           "Improper use of this information will be penalized with a fine of two to ten Monthly Tax Units (UTM) in accordance with the Law.",
           "Courtesy translation of the official Spanish document issued by Chile's Servicio de Registro Civil e Identificación. Only the Spanish original is the official document; in case of doubt, the Spanish text prevails."],
    "pt": ["Consulta de inabilidades para trabalhar com menores de idade", "Prezado(a) usuário(a):",
           "O Serviço de Registro Civil e Identificação (Servicio de Registro Civil e Identificación) informa que o(a) Sr.(a):",
           "RUN", "NOME", "NÃO possui inabilidades para trabalhar com menores de idade.", "Data",
           "Lembramos que esta consulta pode ser feita caso seja necessário contratar a pessoa para um emprego ou cargo que envolva relação direta e habitual com menores de idade, ou fins semelhantes.",
           "O uso indevido desta informação será sancionado com multa de duas a dez Unidades Tributárias Mensais (UTM), de acordo com a Lei.",
           "Tradução de cortesia do documento oficial em espanhol emitido pelo Servicio de Registro Civil e Identificación do Chile. Somente o original em espanhol é o documento oficial; em caso de dúvida, prevalece o texto em espanhol."],
    "it": ["Consultazione delle interdizioni a lavorare con minori", "Gentile utente,",
           "Il Servizio di Registro Civile e Identificazione (Servicio de Registro Civil e Identificación) comunica che il/la Sig./Sig.ra:",
           "RUN", "NOME", "NON risulta alcuna interdizione a lavorare con minori.", "Data",
           "Le ricordiamo che questa consultazione può essere effettuata se è necessario assumere la persona per un impiego o un incarico che comporti un rapporto diretto e abituale con minori, o per fini analoghi.",
           "L'uso improprio di queste informazioni sarà sanzionato con una multa da due a dieci Unità Tributarie Mensili (UTM) ai sensi di legge.",
           "Traduzione di cortesia del documento ufficiale in spagnolo rilasciato dal Servicio de Registro Civil e Identificación del Cile. Solo l'originale in spagnolo è il documento ufficiale; in caso di dubbio prevale il testo spagnolo."],
    "fr": ["Consultation des interdictions d'exercer auprès de mineurs", "Cher utilisateur, chère utilisatrice,",
           "Le Service d'état civil et d'identification (Servicio de Registro Civil e Identificación) informe que M./Mme :",
           "RUN", "NOM", "N'a AUCUNE interdiction de travailler avec des mineurs.", "Date",
           "Nous vous rappelons que cette consultation peut être effectuée si vous devez embaucher la personne pour un emploi ou un poste impliquant une relation directe et habituelle avec des mineurs, ou à des fins similaires.",
           "L'usage abusif de ces informations sera sanctionné d'une amende de deux à dix Unités Tributaires Mensuelles (UTM) conformément à la loi.",
           "Traduction de courtoisie du document officiel en espagnol délivré par le Servicio de Registro Civil e Identificación du Chili. Seul l'original en espagnol est le document officiel ; en cas de doute, le texte espagnol prévaut."],
    "zh": ["关于从事涉及未成年人工作的禁止资格查询", "尊敬的用户：",
           "智利民事登记与身份识别局（Servicio de Registro Civil e Identificación）特此告知，以下人员：",
           "RUN", "姓名", "没有任何不得从事涉及未成年人工作的禁止记录。", "日期",
           "提醒您：如需聘用该人员从事与未成年人有直接且经常性接触的工作或职位，或出于类似目的，可进行此项查询。",
           "不当使用此信息将依法被处以二至十个月度税务单位（UTM）的罚款。",
           "本文件为智利 Servicio de Registro Civil e Identificación 签发的西班牙语官方文件的参考译文。仅西班牙语原件为官方文件；如有疑义，以西班牙语文本为准。"],
    "zh-TW": ["關於從事涉及未成年人工作的禁止資格查詢", "敬愛的使用者：",
              "智利民事登記與身分識別局（Servicio de Registro Civil e Identificación）特此告知，以下人員：",
              "RUN", "姓名", "沒有任何不得從事涉及未成年人工作的禁止紀錄。", "日期",
              "提醒您：如需聘用該人員從事與未成年人有直接且經常性接觸的工作或職位，或基於類似目的，可進行此項查詢。",
              "不當使用此資訊將依法處以二至十個月度稅務單位（UTM）的罰款。",
              "本文件為智利 Servicio de Registro Civil e Identificación 所核發西班牙文官方文件的參考譯文。僅西班牙文原件為官方文件；如有疑義，以西班牙文為準。"],
    "ja": ["未成年者を対象とする業務に関する就業制限の照会", "ご利用者様",
           "チリ民事登録・身分証明局（Servicio de Registro Civil e Identificación）は、次の方について通知します。",
           "RUN", "氏名", "未成年者を対象とする業務に就くことについての制限は登録されていません。", "日付",
           "この照会は、未成年者との直接かつ日常的な関わりを伴う職務・役職での雇用や、これに類する目的のために行うことができます。",
           "この情報を不正に使用した場合、法律に基づき、月次税単位（UTM）の2倍から10倍の罰金が科されます。",
           "本書は、チリの Servicio de Registro Civil e Identificación が発行したスペイン語の公式文書の参考訳です。公式文書はスペイン語の原本のみであり、疑義がある場合はスペイン語の文面が優先されます。"],
    "ko": ["미성년자 관련 업무 결격 사유 조회", "이용자님께",
           "칠레 민사등록·신원확인청(Servicio de Registro Civil e Identificación)은 다음 사람에 대해 알려 드립니다.",
           "RUN", "성명", "미성년자와 관련된 업무에 대한 결격 사유가 등록되어 있지 않습니다.", "일시",
           "이 조회는 미성년자와 직접적이고 일상적인 관계를 수반하는 직무나 직위로 해당인을 채용하거나 이와 유사한 목적이 있는 경우에 할 수 있습니다.",
           "이 정보를 부당하게 사용하면 법에 따라 월간 세금 단위(UTM)의 2배에서 10배의 벌금이 부과됩니다.",
           "이 문서는 칠레 Servicio de Registro Civil e Identificación이 발급한 스페인어 공식 문서의 참고용 번역본입니다. 공식 문서는 스페인어 원본뿐이며, 의문이 있을 경우 스페인어 본문이 우선합니다."],
    "tr": ["Reşit olmayanlarla çalışma yasağı sorgusu", "Sayın kullanıcı,",
           "Şili Sivil Sicil ve Kimlik Hizmeti (Servicio de Registro Civil e Identificación), aşağıdaki kişi hakkında bilgi verir:",
           "RUN", "AD SOYAD", "Reşit olmayanlarla çalışmaya yönelik herhangi bir yasağı BULUNMAMAKTADIR.", "Tarih",
           "Bu sorgu, kişiyi reşit olmayanlarla doğrudan ve düzenli ilişki gerektiren bir iş veya görev için ya da benzer amaçlarla işe almanız gerektiğinde yapılabilir.",
           "Bu bilginin kötüye kullanılması, kanuna uygun olarak iki ila on Aylık Vergi Birimi (UTM) tutarında para cezasıyla cezalandırılır.",
           "Bu belge, Şili'deki Servicio de Registro Civil e Identificación tarafından düzenlenen resmî İspanyolca belgenin kolaylık amaçlı çevirisidir. Yalnızca İspanyolca aslı resmî belgedir; şüphe halinde İspanyolca metin esastır."],
    "ru": ["Справка о запретах на работу с несовершеннолетними", "Уважаемый пользователь!",
           "Служба гражданской регистрации и идентификации Чили (Servicio de Registro Civil e Identificación) сообщает, что г-н/г-жа:",
           "RUN", "ФИО", "НЕ имеет запретов на работу с несовершеннолетними.", "Дата",
           "Напоминаем, что этот запрос можно делать, если необходимо принять человека на работу или должность, связанную с непосредственным и регулярным общением с несовершеннолетними, либо в аналогичных целях.",
           "Ненадлежащее использование этой информации влечёт штраф в размере от двух до десяти Ежемесячных налоговых единиц (UTM) в соответствии с законом.",
           "Справочный перевод официального документа на испанском языке, выданного чилийской службой Servicio de Registro Civil e Identificación. Официальным является только испанский оригинал; в случае сомнений приоритет имеет испанский текст."],
    "vi": ["Tra cứu hạn chế làm việc với người chưa thành niên", "Kính gửi quý người dùng,",
           "Cơ quan Đăng ký Hộ tịch và Nhận dạng (Servicio de Registro Civil e Identificación) thông báo rằng ông/bà:",
           "RUN", "HỌ TÊN", "KHÔNG bị ghi nhận hạn chế nào về việc làm việc với người chưa thành niên.", "Ngày",
           "Chúng tôi nhắc rằng có thể thực hiện tra cứu này nếu cần tuyển dụng người đó vào công việc hoặc vị trí liên quan đến tiếp xúc trực tiếp và thường xuyên với người chưa thành niên, hoặc cho các mục đích tương tự.",
           "Việc sử dụng sai mục đích thông tin này sẽ bị phạt từ hai đến mười Đơn vị Thuế Hằng tháng (UTM) theo quy định của pháp luật.",
           "Bản dịch tham khảo của văn bản chính thức bằng tiếng Tây Ban Nha do Servicio de Registro Civil e Identificación của Chile cấp. Chỉ bản gốc tiếng Tây Ban Nha là văn bản chính thức; khi có nghi vấn, văn bản tiếng Tây Ban Nha được ưu tiên."],
    "th": ["การตรวจสอบข้อห้ามในการทำงานกับผู้เยาว์", "เรียนผู้ใช้บริการ",
           "สำนักงานทะเบียนราษฎรและพิสูจน์ตัวตนของชิลี (Servicio de Registro Civil e Identificación) ขอแจ้งว่า คุณ:",
           "RUN", "ชื่อ-นามสกุล", "ไม่มีข้อห้ามในการทำงานกับผู้เยาว์", "วันที่",
           "ขอแจ้งให้ทราบว่า สามารถตรวจสอบนี้ได้หากจำเป็นต้องจ้างบุคคลดังกล่าวเข้าทำงานหรือดำรงตำแหน่งที่เกี่ยวข้องกับการติดต่อโดยตรงและเป็นประจำกับผู้เยาว์ หรือเพื่อวัตถุประสงค์ที่คล้ายกัน",
           "การนำข้อมูลนี้ไปใช้โดยมิชอบจะถูกปรับตั้งแต่สองถึงสิบหน่วยภาษีรายเดือน (UTM) ตามกฎหมาย",
           "ฉบับแปลเพื่ออำนวยความสะดวกของเอกสารทางการภาษาสเปนที่ออกโดย Servicio de Registro Civil e Identificación ของชิลี เฉพาะต้นฉบับภาษาสเปนเท่านั้นที่เป็นเอกสารทางการ หากมีข้อสงสัยให้ยึดข้อความภาษาสเปนเป็นหลัก"],
    "de": ["Abfrage von Tätigkeitsverboten für die Arbeit mit Minderjährigen", "Sehr geehrte Nutzerin, sehr geehrter Nutzer,",
           "der chilenische Zivilstands- und Identifikationsdienst (Servicio de Registro Civil e Identificación) teilt mit, dass Herr/Frau:",
           "RUN", "NAME", "KEINE Tätigkeitsverbote für die Arbeit mit Minderjährigen eingetragen hat.", "Datum",
           "Wir weisen darauf hin, dass diese Abfrage erfolgen kann, wenn die Person für eine Stelle oder Funktion mit direktem und regelmäßigem Kontakt zu Minderjährigen oder zu ähnlichen Zwecken eingestellt werden soll.",
           "Der missbräuchliche Gebrauch dieser Information wird gemäß Gesetz mit einer Geldstrafe von zwei bis zehn Monatlichen Steuereinheiten (UTM) geahndet.",
           "Unverbindliche Übersetzung des offiziellen spanischen Dokuments, das vom chilenischen Servicio de Registro Civil e Identificación ausgestellt wurde. Nur das spanische Original ist das offizielle Dokument; im Zweifel gilt der spanische Text."],
    "uk": ["Довідка про заборони на роботу з неповнолітніми", "Шановний користувачу!",
           "Служба цивільної реєстрації та ідентифікації Чилі (Servicio de Registro Civil e Identificación) повідомляє, що пан/пані:",
           "RUN", "ПІБ", "НЕ має заборон на роботу з неповнолітніми.", "Дата",
           "Нагадуємо, що цей запит можна робити, якщо потрібно прийняти особу на роботу чи посаду, пов'язану з безпосереднім і регулярним спілкуванням з неповнолітніми, або з подібною метою.",
           "Неналежне використання цієї інформації карається штрафом від двох до десяти Місячних податкових одиниць (UTM) відповідно до закону.",
           "Довідковий переклад офіційного документа іспанською мовою, виданого чилійською службою Servicio de Registro Civil e Identificación. Офіційним є лише іспанський оригінал; у разі сумнівів перевагу має іспанський текст."],
    "pl": ["Zapytanie o zakazy pracy z małoletnimi", "Szanowny Użytkowniku,",
           "Służba Rejestru Cywilnego i Identyfikacji Chile (Servicio de Registro Civil e Identificación) informuje, że Pan/Pani:",
           "RUN", "IMIĘ I NAZWISKO", "NIE ma zakazów pracy z małoletnimi.", "Data",
           "Przypominamy, że zapytanie to można złożyć, jeśli zachodzi potrzeba zatrudnienia osoby na stanowisku lub w funkcji wiążącej się z bezpośrednim i stałym kontaktem z małoletnimi albo w podobnych celach.",
           "Niewłaściwe wykorzystanie tych informacji będzie zagrożone grzywną w wysokości od dwóch do dziesięciu Miesięcznych Jednostek Podatkowych (UTM) zgodnie z prawem.",
           "Tłumaczenie poglądowe oficjalnego dokumentu w języku hiszpańskim wydanego przez chilijską instytucję Servicio de Registro Civil e Identificación. Dokumentem oficjalnym jest wyłącznie hiszpański oryginał; w razie wątpliwości rozstrzyga tekst hiszpański."],
    "ar": ["الاستعلام عن موانع العمل مع القاصرين", "عزيزي المستخدم،",
           "تُفيد دائرة السجل المدني والتعريف في تشيلي (Servicio de Registro Civil e Identificación) بأن السيد/السيدة:",
           "RUN", "الاسم", "لا توجد لديه/لديها أي موانع للعمل مع القاصرين.", "التاريخ",
           "نُذكّركم بأنه يمكن إجراء هذا الاستعلام إذا لزم توظيف الشخص في عمل أو منصب يتضمن علاقة مباشرة ومعتادة مع القاصرين، أو لأغراض مشابهة.",
           "يُعاقَب على إساءة استخدام هذه المعلومات بغرامة من وحدتين إلى عشر وحدات ضريبية شهرية (UTM) وفقاً للقانون.",
           "ترجمة للاطلاع للوثيقة الرسمية الإسبانية الصادرة عن Servicio de Registro Civil e Identificación في تشيلي. الأصل الإسباني وحده هو الوثيقة الرسمية؛ وعند الشك يُعتد بالنص الإسباني."],
    "fa": ["استعلام ممنوعیت‌های کار با افراد زیر سن قانونی", "کاربر گرامی،",
           "اداره ثبت احوال و شناسایی شیلی (Servicio de Registro Civil e Identificación) اعلام می‌دارد که آقا/خانم:",
           "RUN", "نام", "هیچ ممنوعیتی برای کار با افراد زیر سن قانونی ثبت نشده است.", "تاریخ",
           "یادآوری می‌کنیم که این استعلام را می‌توان در صورت نیاز به استخدام فرد برای شغل یا سمتی که مستلزم ارتباط مستقیم و مستمر با افراد زیر سن قانونی است، یا برای مقاصد مشابه انجام داد.",
           "استفاده نادرست از این اطلاعات طبق قانون با جریمه‌ای از دو تا ده واحد مالیاتی ماهانه (UTM) مجازات می‌شود.",
           "ترجمه ارفاقی سند رسمی اسپانیایی صادرشده توسط Servicio de Registro Civil e Identificación شیلی. تنها نسخه اصلی اسپانیایی سند رسمی است؛ در صورت تردید، متن اسپانیایی ملاک است."],
    "id": ["Pemeriksaan larangan bekerja dengan anak di bawah umur", "Pengguna yang terhormat,",
           "Layanan Catatan Sipil dan Identifikasi (Servicio de Registro Civil e Identificación) Chile menyampaikan bahwa Bapak/Ibu:",
           "RUN", "NAMA", "TIDAK tercatat memiliki larangan untuk bekerja dengan anak di bawah umur.", "Tanggal",
           "Kami mengingatkan bahwa pemeriksaan ini dapat dilakukan jika Anda perlu mempekerjakan orang tersebut untuk pekerjaan atau jabatan yang melibatkan hubungan langsung dan rutin dengan anak di bawah umur, atau untuk tujuan serupa.",
           "Penyalahgunaan informasi ini akan dikenai denda dua hingga sepuluh Unit Pajak Bulanan (UTM) sesuai dengan Undang-Undang.",
           "Terjemahan sebagai kemudahan atas dokumen resmi berbahasa Spanyol yang diterbitkan oleh Servicio de Registro Civil e Identificación Chile. Hanya naskah asli berbahasa Spanyol yang merupakan dokumen resmi; jika ada keraguan, teks berbahasa Spanyol yang berlaku."],
    "nl": ["Raadpleging van beroepsverboden voor werk met minderjarigen", "Geachte gebruiker,",
           "De Chileense dienst voor burgerlijke stand en identificatie (Servicio de Registro Civil e Identificación) deelt mee dat de heer/mevrouw:",
           "RUN", "NAAM", "GEEN verboden heeft om met minderjarigen te werken.", "Datum",
           "Wij herinneren u eraan dat deze raadpleging kan worden uitgevoerd als u de persoon wilt aanstellen voor een baan of functie met directe en regelmatige omgang met minderjarigen, of voor soortgelijke doeleinden.",
           "Oneigenlijk gebruik van deze informatie wordt overeenkomstig de wet bestraft met een boete van twee tot tien Maandelijkse Belastingeenheden (UTM).",
           "Vertaling ter oriëntatie van het officiële Spaanse document, afgegeven door het Chileense Servicio de Registro Civil e Identificación. Alleen het Spaanse origineel is het officiële document; bij twijfel prevaleert de Spaanse tekst."],
    "hi": ["नाबालिगों के साथ काम करने की अयोग्यताओं की जाँच", "प्रिय उपयोगकर्ता,",
           "चिली की नागरिक पंजीकरण एवं पहचान सेवा (Servicio de Registro Civil e Identificación) सूचित करती है कि श्री/सुश्री:",
           "RUN", "नाम", "नाबालिगों के साथ काम करने के लिए कोई अयोग्यता दर्ज नहीं है।", "दिनांक",
           "हम स्मरण कराते हैं कि यह जाँच तब की जा सकती है जब किसी व्यक्ति को ऐसे रोज़गार या पद पर नियुक्त करना हो जिसमें नाबालिगों के साथ प्रत्यक्ष और नियमित संपर्क शामिल हो, या इसी प्रकार के उद्देश्यों के लिए।",
           "इस जानकारी के दुरुपयोग पर कानून के अनुसार दो से दस मासिक कर इकाइयों (UTM) के जुर्माने का दंड दिया जाएगा।",
           "चिली की Servicio de Registro Civil e Identificación द्वारा जारी स्पेनिश आधिकारिक दस्तावेज़ का सुविधा हेतु अनुवाद। केवल स्पेनिश मूल प्रति ही आधिकारिक दस्तावेज़ है; संदेह की स्थिति में स्पेनिश पाठ मान्य होगा।"],
    "el": ["Έλεγχος κωλυμάτων εργασίας με ανηλίκους", "Αγαπητέ χρήστη,",
           "Η Υπηρεσία Ληξιαρχείου και Ταυτοποίησης της Χιλής (Servicio de Registro Civil e Identificación) ενημερώνει ότι ο/η κ.:",
           "RUN", "ΟΝΟΜΑ", "ΔΕΝ έχει καταχωρισμένα κωλύματα για εργασία με ανηλίκους.", "Ημερομηνία",
           "Σας υπενθυμίζουμε ότι ο έλεγχος αυτός μπορεί να γίνει εάν πρέπει να προσληφθεί το πρόσωπο για θέση ή καθήκοντα που συνεπάγονται άμεση και συνήθη σχέση με ανηλίκους, ή για παρόμοιους σκοπούς.",
           "Η κακή χρήση των πληροφοριών αυτών τιμωρείται με πρόστιμο δύο έως δέκα Μηνιαίων Φορολογικών Μονάδων (UTM) σύμφωνα με τον νόμο.",
           "Ενδεικτική μετάφραση του επίσημου ισπανικού εγγράφου που εκδόθηκε από το Servicio de Registro Civil e Identificación της Χιλής. Επίσημο έγγραφο είναι μόνο το ισπανικό πρωτότυπο· σε περίπτωση αμφιβολίας υπερισχύει το ισπανικό κείμενο."],
}


def read_source_facts(source: Path) -> dict:
    """Read RUN, name and issue date from the official PDF (never retyped)."""
    text = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(source), "-"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    run = re.search(r"RUN\s+([\d.]+-[\dkK])", text)
    name = re.search(r"NOMBRE\s+(.+)", text)
    stamp = re.search(r"Fecha\s+(\d{1,2})\s+(\w+)\s+(\d{4}),\s+(\d{1,2}:\d{2})", text)
    if not (run and name and stamp and "NO registra inhabilidades" in text):
        raise SystemExit("El PDF fuente no tiene el formato esperado; no se genera ninguna traduccion.")
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
              "septiembre", "octubre", "noviembre", "diciembre"]
    month = months.index(stamp.group(2).lower()) + 1
    return {
        "run": run.group(1),
        "name": name.group(1).strip(),
        "date": f"{stamp.group(3)}-{month:02d}-{int(stamp.group(1)):02d} · {stamp.group(4)}",
    }


def browser_executable() -> Path:
    for candidate in (
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ):
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Chrome o Edge es necesario para renderizar los PDF multilingües")


def page(code: str, direction: str, texts: list, facts: dict) -> str:
    title, dear, intro, run_l, name_l, result, date_l, remind, warn, banner = texts
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="{e(code)}" dir="{direction}"><head><meta charset="utf-8"><title>{e(title)}</title><style>
@page {{ size: A4; margin: 20mm 18mm; }}
body {{ font-family: "Segoe UI","Nirmala UI","Yu Gothic","Malgun Gothic","Microsoft YaHei","Microsoft JhengHei","Leelawadee UI",Tahoma,Arial,sans-serif; color:#162033; font-size:11pt; line-height:1.55; }}
.banner {{ border:1px solid #b45309; background:#fffbeb; color:#78350f; padding:3mm 4mm; font-size:8.8pt; margin:0 0 9mm; }}
h1 {{ font-size:17pt; color:#15375b; border-bottom:3px solid #2563eb; padding-bottom:3mm; margin:0 0 8mm; }}
table.id {{ border-collapse:collapse; margin:6mm 0 8mm; }}
table.id td {{ padding:1.5mm 6mm 1.5mm 0; font-weight:600; }}
table.id td:first-child {{ color:#475569; }}
.result {{ border-inline-start:5px solid #15803d; background:#f0fdf4; padding:4mm 5mm; font-weight:700; font-size:12.5pt; margin:0 0 8mm; }}
.small {{ font-size:9.5pt; color:#334155; }}
.foot {{ margin-top:12mm; padding-top:3mm; border-top:1px solid #cbd5e1; font-size:8pt; color:#526071; }}
</style></head><body>
<p class="banner">{e(banner)}<br><span dir="ltr">{e(PUBLIC_URL)}</span></p>
<h1>{e(title)}</h1>
<p>{e(dear)}</p>
<p>{e(intro)}</p>
<table class="id"><tr><td>{e(run_l)}</td><td dir="ltr">{e(facts['run'])}</td></tr><tr><td>{e(name_l)}</td><td dir="ltr">{e(facts['name'])}</td></tr></table>
<p class="result">{e(result)}</p>
<p><b>{e(date_l)}:</b> <span dir="ltr">{e(facts['date'])}</span></p>
<p class="small">{e(remind)}</p>
<p class="small">{e(warn)}</p>
<p class="foot">Servicio de Registro Civil e Identificación · Consulta inhabilidades para trabajar con menores de edad · ES: {e(PUBLIC_URL)}</p>
</body></html>"""


def render(target: Path, markup: str, code: str) -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    src = TMP / f"inhabilidades-{code}.html"
    src.write_text(markup, encoding="utf-8")
    target.unlink(missing_ok=True)
    subprocess.run(
        [str(browser_executable()), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--user-data-dir={TMP / 'edge-profile'}", f"--print-to-pdf={target.resolve()}", src.resolve().as_uri()],
        capture_output=True, text=True, timeout=90,
    )
    deadline = time.monotonic() + 60
    last, stable = -1, 0
    while time.monotonic() < deadline:
        size = target.stat().st_size if target.exists() else 0
        stable = stable + 1 if size > 1000 and size == last else 0
        if stable >= 2:
            break
        last = size
        time.sleep(0.5)
    if not target.exists() or target.stat().st_size < 1000:
        raise RuntimeError(f"No se pudo renderizar {target.name}")
    src.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="PDF oficial en español")
    args = parser.parse_args()
    facts = read_source_facts(args.source)

    spanish = ASSETS / f"{BASE_NAME}.pdf"
    shutil.copyfile(args.source, spanish)  # el original oficial se copia sin alterar
    print(f"OK es: {spanish.name} (copia sin alterar)")

    for locale in CONTRACT["locales"]:
        code = locale["code"]
        if code == "es":
            continue
        target = ASSETS / f"{BASE_NAME}{locale['suffix']}.pdf"
        render(target, page(code, locale["direction"], T[code], facts), code)
        print(f"OK {code}: {target.name}")


if __name__ == "__main__":
    main()
