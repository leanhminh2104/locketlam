from __future__ import annotations

from datetime import datetime

import os
import io
import time
import uuid
import random
import string
import urllib.parse
import requests
try:
    # pyrefly: ignore [missing-import]
    from PIL import Image
except ImportError:
    Image = None

try:
    from ..exceptions import StorageUploadError, LocketAPIError
except ImportError:
    try:
        from locketlam.exceptions import StorageUploadError, LocketAPIError
    except ImportError:
        class StorageUploadError(Exception): pass
        class LocketAPIError(Exception): pass

class NoteType:
    """Supported note and caption overlay styles in Locket (complete presets library)."""
    # ==========================================
    # 🎨 General
    # ==========================================
    STANDARD = "standard"
    REVIEW = "review"
    MUSIC = "music"
    LOCATION = "location"
    WEATHER = "weather"
    TIME = "time"
    STREAK = "streak"
    STAR_SIGN = "star_sign"
    POLL = "poll"
    LOCKET_COUNT = "locket_count"
    COLORS = "colors"

    # ==========================================
    # 🎨 Holiday Caption
    # ==========================================
    HALLOWEEN_2026 = "halloween_2026"  # 🎃 Halloween
    CHRISTMAS_EVE_2026 = "christmas_eve_2026"  # 🕯️ Giáng sinh an lành
    CHRISTMAS_DAY_2026 = "christmas_day_2026"  # 🎄 Giáng sinh an lành
    NEW_YEARS_EVE_2026 = "new_years_eve_2026"  # 🥂 Xin chào 2027!
    NEW_YEARS_DAY_2027 = "new_years_day_2027"  # 💫 Xin chào 2027!
    NEW_YEARS_DAY_2027_ALTERNATE = "new_years_day_2027_alternate"  # 2027
    AUTUMN_2026 = "autumn_2026"  # 🍂 Xin chào Mùa Thu

    # ==========================================
    # General
    # ==========================================
    COLOR_PALETTE = "color_palette"

    # ==========================================
    # 🎨 Decorative by Locket
    # ==========================================
    PARTY_TIME = "party_time"  # 🪩 Party Time!
    GOOD_MORNING = "good_morning"  # ☀️ Good morning
    GOODNIGHT = "goodnight"  # 🌙 Goodnight
    OOTD = "ootd"  # 🕶 OOTD
    MISS_YOU = "miss_you"  # 🥰 Miss you
    TOI_NHO_EM = "toi_nho_em"  # 보고 싶어 🥺

    # ==========================================
    # In Love 💘
    # ==========================================
    DOI_ROI = "custom_4281443912454362723"  # 😤 Dỗi rồi
    DANG_BAN_TUONG_TU = "custom_4278420056830692855"  # 💭 Đang bận tương tư
    REP_TIN_NHAN_DI = "custom_-5230082930652109611"  # 📩 Rep tin nhắn đi
    MO_HON_NHUNG_TAM_HIEN = "custom_-3194172128167113174"  # 🐤 Mỏ hỗn nhưng tâm hiền
    MUON_DUOC_OM = "custom_951140262642706115"  # 🫂 Muốn được ôm
    HOI_BI_NHO = "custom_-2517074947356721928"  # 🤏 Hơi bị nhớ
    DANG_GHEN = "custom_8704346769822013791"  # 🔥 Đang ghen
    NGU_NGON_GIAC_MO_CO_EM = "custom_-6322769402934766020"  # 🌌 Ngủ ngon giấc mơ có em

    # ==========================================
    # Gen Z Life 🩻
    # ==========================================
    HAO_HAN = "custom_-7748601173102319221"  # 🗡️ Hảo hán
    CAM_LANH = "custom_5086729225261087312"  # 🤧 Cảm lạnh
    BAT_LUC = "custom_-8827799067762644667"  # 🏳️ Bất lực
    XIN_LUI_DUOC_CHUA = "custom_1207712346050008572"  # 🥺 Xin lũi được chưa
    ROT_NUOC_MAT = "custom_7843091339669964287"  # 😭 Rớt nước mắt
    GUC_NGA = "custom_-6209580156274658388"  # 📉 Gục ngã
    TIEN_DINH = "custom_2624241615109400076"  # 🌪️ Tiền đình
    CHE_MANH = "custom_6333530155972530884"  # 👎 Chê mạnh
    XINH_GAI_AN_PHIM_1 = "custom_5236262895016786086"  # 💅 Xinh gái ấn phím 1
    DI_LAM_VI_DAM_ME = "custom_4629360466318251663"  # 🤡 Đi làm vì đam mê

    # ==========================================
    # Wordsmith 📖
    # ==========================================
    YEUU_EMM = "custom_2356683405459396780"  # 💖 Yeuu Emm
    YEUU_ANHH = "custom_-156517413958162274"  # 💙 Yeuu Anhh
    HOI_CHIEU_TROI_MUA = "custom_-1002616293585878253"  # 🌧️ Hồi chiều trời mưa
    CON_VIEN_LA_LAN = "custom_2988924028358029735"  # 🍂 côn viên lá làn
    AIIII_HOIIII = "custom_-776650182805465343"  # 🐽 aiiii hoiiii ?
    TAI_ONG_DE_NGOAI_DAU_A = "custom_8807240841082552583"  # 👂 Tai ông để ngoài đầu à
    CHAN_BO_MAY_DI = "custom_9142722434980417998"  # 🙄 Chan bố mày đi
    OACH_XA_LACH = "custom_-2275483743616875628"  # 🥬 oách xà lách
    E_HE = "custom_-1964354746873974650"  # 🤭 è hé
    UA_ALO = "custom_-8051687911840908357"  # 📞 Ủa alo
    MAY_CHU_LA_DU_DU = "custom_5306143805773536410"  # 🍃 Máy chủ lá đu đủ
    LANH_THAY_ME = "custom_8500361098265117961"  # 🥶 lạnh thấy mẹ
    DAY_LA_CAI_VIEC = "custom_9196689374819632769"  # 🤷‍♂️ Đấy Là Cái Việc
    DEP_TRAI_AN_PHIM_2 = "custom_-1593423561129370554"  # 📱 Đẹp trai ấn phím 2
    NHO_ANH_CH = "custom_1826983258186006295"  # 🥺 Nho anh ch?
    BIEN_OI_HUUUUUUU = "custom_-7090905829866915796"  # 🌊 Biển ơi húuuuuuu
    YEU_ME = "custom_5774090202020534389"  # ❤️ Yêu Mẹ
    NHO_NGY = "custom_158060084751342837"  # 💔 nhớ ngy
    OAN_TA_LA_VAN = "custom_-8740976725662466401"  # 🌀 Oằn tà là vằn
    KHA_NANG_CAO = "custom_2881592073605293252"  # 🤔 Khả Năng Cao
    O_QUA_KIEU = "custom_530435604131815207"  # 💅 ơ quá kiêu
    LANH_NHO_AI = "custom_3095077949020722512"  # ❄️ lạnh nhớ ai
    DUNG_NHANG_NHIT = "custom_-1835481008846003750"  # 🙅‍♂️ Đừng nhăng nhít
    HOM_NAY_TOI_BUON = "custom_2800157096924376465"  # 🥀 hôm nay tôi buồn
    GAP_NHAU_CAI_NHI = "custom_-1606761404320333220"  # 🍻 gặp nhau cái nhỉ
    ANK_IU_EIM = "custom_-985711000650511532"  # 🥰 ank iu eim
    MONG_TON_HOA_SEN_THAY_CANH_NAY = "custom_8417033934333284867"  # 🪷 Mong tôn hoa sen thấy cảnh này
    DAM_NHAU_KHONG = "custom_-8088027983880581018"  # 🥊 đấm nhau không
    SIEU_CAP_BA_KHI = "custom_2329667605952175965"  # 🐉 siêu cấp bá khí
    DU_AN_MA = "custom_-3231089972810420922"  # 👻 dự án ma
    DOC_SO_TAI_KHOAN = "custom_5553591653597204903"  # 💳 đọc số tài khoản
    AI_SO_THI_DI_VE = "custom_-666096677004943582"  # 🚶‍♂️ ai sợ thì đi về
    CON_CAI_NIT = "custom_-3548848387881782452"  # 🧶 còn cái nịt
    CANH_BAO_CO_HAT = "custom_1285814533953315227"  # 🎤 cảnh báo có hát
    THAN_CHUA_MA_DON = "custom_-7627856025199367222"  # 😒 Thân chưa mà dỡn
    AI_MUON = "custom_1443622437168042269"  # 🤨 Ai mượn?
    HAY_RA_DE_QUA_A = "custom_2923223443268332123"  # 🙄 Hay ra dẻ quá à!
    GIAM_SUC_MANH_CON_TUONG_NAY = "custom_5807806141447560156"  # 🎮 Giảm sức mạnh con tướng này
    MAC_CO_QUA_HAI_OI = "custom_7816289860114210553"  # 🫣 Mắc cỡ quá hai ơi
    MINH_LA_LOP = "custom_-5360614187519837840"  # 🛞 Mình là lốp
    DEP_TRAI_CO_GI_SAI = "custom_-6998405490882227027"  # 😎 Đẹp trai có gì sai

    # ==========================================
    # 🎨 Decorative Presets
    # ==========================================
    FEELING_CUTE = "feeling_cute"  # 🌷 Feeling Cute
    CU = "cu"  # Cu 🐎
    WEDDING_TIME = "wedding_time"  # 💍 Wedding Time!
    CAM_THAY_HANH_PHUC = "cam_thay_hanh_phuc"  # 🇻🇳 Cảm thấy hạnh phúc
    COFFEE_TIME = "coffee_time"  # ☕ Coffee Time!
    SNAKE_VIBES = "snake_vibes"  # 🐍 Snake Vibes
    MIXUE_TIME = "mixue_time"  # 🍦 Mixue Time!
    LOCKET_TIME = "locket_time"  # 📷 Locket Time!
    CINEMA_TIME = "cinema_time"  # 🎬 Cinema Time!
    DATING_TIME = "dating_time"  # 💕 Dating Time!
    GRADUATION_DAY = "graduation_day"  # 🎓 Happy Graduation Day!
    SHOPPING_TIME = "shopping_time"  # 🛍️ Shopping Time!
    DINNER_TIME = "dinner_time"  # 🍽️ Dinner Time!
    CHILLING_TIME = "chilling_time"  # 🌴 Chilling Time!

    # ==========================================
    # 🌸 Độc lạ
    # ==========================================
    XIN_VINH_BIET_CU = "xin_vinh_biet_cu"  # 🕯️ Xin vĩnh biệt cụ
    CHAY_NGAY_DI = "chay_ngay_di"  # 🏃💨 Chạy ngay đi
    CU_TU_TU_KHOAI_SE_NHU = "cu_tu_tu_khoai_se_nhu"  # 🥔 Cứ từ từ khoai sẽ nhừ
    KIEM_TRA_NHAN_PHAM = "kiem_tra_nhan_pham"  # 🎲 Kiểm tra nhân phẩm
    DOC_SO_TAI_KHOAN_2 = "doc_so_tai_khoan"  # 💳 đọc số tài khoản
    AI_SO_THI_DI_VE_2 = "ai_so_thi_di_ve"  # 🏃 ai sợ thì đi về
    CON_CAI_NIT_2 = "con_cai_nit"  # 🧶 còn cái nịt
    CANH_BAO_CO_HAT_2 = "canh_bao_co_hat"  # 🎤 cảnh báo có hát
    THAN_CHUA_MA_DON_2 = "than_chua_ma_don"  # 😔 Thân chưa mà dỡn
    AI_MUON_2 = "ai_muon"  # 🤔 Ai mượn?
    HAY_RA_DE_QUA_A_2 = "hay_ra_de_qua_a"  # 🥺 Hay ra dẻ quá à!
    GIAM_SUC_MANH_CON_TUONG = "giam_suc_manh_con_tuong"  # 🎮 Giảm sức mạnh con tướng
    MAC_CO_QUA_HAI_OI_2 = "mac_co_qua_hai_oi"  # 😭 Mắc cỡ quá hai ơi
    MINH_LA_LOP_2 = "minh_la_lop"  # 🛞 Mình là lốp
    DEP_TRAI_CO_GI_SAI_2 = "dep_trai_co_gi_sai"  # 😎 Đẹp trai có gì sai
    MONG_TON_HOA_SEN = "mong_ton_hoa_sen"  # 🪷 Mong tôn hoa sen thấy cảnh này
    DAM_NHAU_KHONG_2 = "dam_nhau_khong"  # 🥊 đấm nhau không
    SIEU_CAP_BA_KHI_2 = "sieu_cap_ba_khi"  # 🐉 siêu cấp bá khí
    DU_AN_MA_2 = "du_an_ma"  # 👻 dự án ma

    # ==========================================
    # 🌸 Trend TikTok
    # ==========================================
    HOI_CHIEU_TROI_MUA_2 = "hoi_chieu_troi_mua"  # 🌧️ Hồi chiều trời mưa...
    TUYET_DOI_KHONG_NGHE = "tuyet_doi_khong_nghe"  # 🙉 Tuyệt đối không nghe
    FLEX_DEN_HOI_THO_CUOI = "flex_den_hoi_tho_cuoi"  # 💎 Flex đến hơi thở cuối
    OVERTHINKING_VAI_CHUONG = "overthinking_vai_chuong"  # 🤯 Overthinking vai chưởng
    KE_CHUYEN_NGHE_CHOI = "ke_chuyen_nghe_choi"  # 🍿 Kể chuyện nghe chơi
    XINH_DEP_TUYET_VOI = "xinh_dep_tuyet_voi"  # 💅 Xinh đẹp tuyệt vời
    TRAM_CAM_NHE = "tram_cam_nhe"  # 🫠 Trầm cảm nhẹ
    CHUA_DU_WOW = "chua_du_wow"  # ⭐ Chưa đủ wow
    BOC_TRUNG_SIT_RIT = "boc_trung_sit_rit"  # 🎁 Bóc trúng sít rịt
    HEN_LAM_MOI_XUI_DUOC_VAY_A = "hen_lam_moi_xui_duoc_vay_a"  # 😅 Hèn lắm mới xui được vậy á
    RA_DUONG_NE_MOI_ANH = "ra_duong_ne_moi_anh"  # 👤 Ra đường nể mỗi anh
    CUNG_CUNG_DI = "cung_cung_di"  # 🚀 Cũng cứng đi
    TUYET_DOI_DIEN_ANH = "tuyet_doi_dien_anh"  # 📷 Tuyệt đối điện ảnh
    DU_BA_KHI_CHUA = "du_ba_khi_chua"  # ⚡ Đủ bá khí chưa
    UA_ALO_2 = "ua_alo"  # ❓ Ủa alo?
    CAI_GI_VAY_TROI = "cai_gi_vay_troi"  # ❗ Cái gì vậy trời
    NAY_LA_HET_CUU = "nay_la_het_cuu"  # ❌ Này là hết cứu
    QUA_LA_DIEN_ANH = "qua_la_dien_anh"  # 📷 Quá là điện ảnh

    # ==========================================
    # 🌸 Meme vui nhộn
    # ==========================================
    CUOI_XIU = "cuoi_xiu"  # 😎 Cười xỉu
    TOANG_THAT_ROI = "toang_that_roi"  # 🐉 Toang thật rồi
    TOI_ROI_TOI_ROI = "toi_roi_toi_roi"  # ❗ Tới rồi tới rồi
    KHONG_THE_TIN_NOI = "khong_the_tin_noi"  # ❓ Không thể tin nổi

    # ==========================================
    # 🌸 Đời sống
    # ==========================================
    NGAY_MOI_VUI_VE = "ngay_moi_vui_ve"  # ☀️ Ngày mới vui vẻ
    NGU_NGON = "ngu_ngon"  # 🌙 Ngủ ngon
    AN_COM_CHUA = "an_com_chua"  # 🍽️ Ăn cơm chưa?
    DI_CHOI_KHONG = "di_choi_khong"  # ✈️ Đi chơi không?

    # ==========================================
    # 🌸 Gen Z Slay
    # ==========================================
    TINH_HOA_HOI_TU = "tinh_hoa_hoi_tu"  # ✨ Tinh hoa hội tụ
    PHU_TINH_KHONG_PHU_BAN = "phu_tinh_khong_phu_ban"  # 🕶️ Phụ tình không phụ bản
    NGOAN_XINH_YEU = "ngoan_xinh_yeu"  # 🌸 Ngoan xinh yêu của ai?
    NHIN_LA_BIET_UY_TIN = "nhin_la_biet_uy_tin"  # 👌 Nhìn là biết uy tín

    # ==========================================
    # 🌸 Bất ổn & Khó đỡ
    # ==========================================
    LUON_VUI_TUOI = "luon_vui_tuoi"  # 🤡 Luôn vui tươi
    BAT_ON_THAT_SU = "bat_on_that_su"  # 🫠 Bất ổn thật sự
    KHONG_CAM_XUC = "khong_cam_xuc"  # 🗿 Không cảm xúc
    PHU_HUYNH_DUNG_XEM = "phu_huynh_dung_xem"  # 🙈 Phụ huynh đừng xem

    # ==========================================
    # 🌸 Check VAR & Hóng hớt
    # ==========================================
    CHECK_VAR = "check_var"  # 📺 Check VAR liền
    QUA_NHIEU_SU_DE_THUONG = "qua_nhieu_su_de_thuong"  # 🎀 Quá nhiều sự dễ thương
    MAC_BAY_TINH_YEU = "mac_bay_tinh_yeu"  # 💘 Mắc bẫy tình yêu
    SONG_GIO_PHU_DOI_TRAI = "song_gio_phu_doi_trai"  # 🌪️ Sóng gió phủ đời trai

    # ==========================================
    # 🌸 Góc Deadline & Đi Làm
    # ==========================================
    DEADLINE_RUOT = "deadline_ruot"  # 🔥 Deadline dí tụt quần
    TIEN_DAU_MA_TIEU = "tien_dau_ma_tieu"  # 💸 Tiền đâu mà tiêu
    NGHIEN_CUU_KHOA_HOC = "nghien_cuu_khoa_hoc"  # ☕ Cần nạp cafein gấp

class MomentsModule:
    """Manages Locket Moments: photo & video uploads, creative note overlays, feed retrieval, and views."""
    STORAGE_IMG_URL = "https://firebasestorage.googleapis.com/v0/b/locket-img/o"
    STORAGE_VIDEO_URL = "https://firebasestorage.googleapis.com/v0/b/locket-video/o"

    def __init__(self, client):
        self.client = client

    def _get_history_file(self) -> str:
        uid = getattr(self.client.session, "uid", "default")
        filename = f"my_moments_{uid}.json"
        # If session_path has a directory, keep history adjacent to it or in cwd
        session_path = getattr(self.client.session, "session_path", "")
        if session_path and os.path.dirname(session_path):
            return os.path.join(os.path.dirname(session_path), filename)
        return filename

    def _load_history(self) -> list:
        import os, json
        filepath = self._get_history_file()
        # Fallback check cwd if not in calculated path
        uid = getattr(self.client.session, "uid", "default")
        candidates = [filepath, f"my_moments_{uid}.json", os.path.join("..", f"my_moments_{uid}.json")]
        for path in candidates:
            if path and os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            return data
                except Exception:
                    pass
        return []

    def _save_history(self, history: list):
        import json
        filepath = self._get_history_file()
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def record_posted_moment(self, moment_data: dict):
        if not isinstance(moment_data, dict):
            return
        mid = moment_data.get("canonical_uid") or moment_data.get("id")
        if not mid:
            return
        history = self._load_history()
        # Prepend or update if existing
        history = [m for m in history if (m.get("canonical_uid") or m.get("id")) != mid]
        history.insert(0, moment_data)
        self._save_history(history)

    @staticmethod
    def _random_id(length: int = 20) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def _convert_to_webp(self, image_data: bytes, quality: int = 85) -> bytes:
        """Automatically converts and compresses any image (JPG, PNG, HEIC) to Locket-standard WebP format."""
        try:
            img = Image.open(io.BytesIO(image_data))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            out = io.BytesIO()
            img.save(out, format="WEBP", quality=quality)
            return out.getvalue()
        except Exception:
            return image_data

    def extract_thumbnail(self, video_input, timestamp_sec: float = 1.0) -> bytes:
        """
        Extracts a high-quality video frame at timestamp_sec and returns WebP compressed bytes.
        Supports local file paths or raw video bytes.
        """
        import tempfile
        import subprocess

        ffmpeg_bin = None
        try:
            import imageio_ffmpeg
            ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass
        if not ffmpeg_bin:
            ffmpeg_bin = "ffmpeg"

        temp_in = None
        temp_out = None
        try:
            if isinstance(video_input, str) and (video_input.startswith("http://") or video_input.startswith("https://")):
                import requests
                parsed_vurl = urllib.parse.urlparse(video_input)
                v_origin = f"{parsed_vurl.scheme}://{parsed_vurl.netloc}/"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Referer": v_origin
                }
                resp = requests.get(video_input, headers=headers, stream=True, timeout=60)
                if resp.status_code != 200:
                    resp = requests.get(video_input, stream=True, timeout=60)
                if resp.status_code == 200:
                    fd_in, temp_in = tempfile.mkstemp(suffix=".mp4")
                    with os.fdopen(fd_in, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                    in_path = temp_in
                else:
                    in_path = video_input
            elif isinstance(video_input, bytes):
                fd_in, temp_in = tempfile.mkstemp(suffix=".mp4")
                with os.fdopen(fd_in, "wb") as f:
                    f.write(video_input)
                in_path = temp_in
            else:
                in_path = video_input

            fd_out, temp_out = tempfile.mkstemp(suffix=".jpg")
            os.close(fd_out)

            cmd = [
                ffmpeg_bin, "-y",
                "-ss", str(timestamp_sec),
                "-i", in_path,
                "-vframes", "1",
                "-q:v", "2",
                temp_out
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if os.path.exists(temp_out) and os.path.getsize(temp_out) > 0:
                with open(temp_out, "rb") as f:
                    jpg_bytes = f.read()
                return self._convert_to_webp(jpg_bytes)
            return b""
        finally:
            if temp_in and os.path.exists(temp_in):
                try:
                    os.remove(temp_in)
                except Exception:
                    pass
            if temp_out and os.path.exists(temp_out):
                try:
                    os.remove(temp_out)
                except Exception:
                    pass

    def upload_image(self, file_path_or_bytes, content_type: str = "image/webp") -> str:
        """Uploads an image to Locket Firebase Storage using Google Resumable Upload protocol. Supports local paths, raw bytes, or online image URLs."""
        import requests
        if isinstance(file_path_or_bytes, str):
            if file_path_or_bytes.startswith("http://") or file_path_or_bytes.startswith("https://"):
                parsed_url = urllib.parse.urlparse(file_path_or_bytes)
                domain_origin = f"{parsed_url.scheme}://{parsed_url.netloc}/"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": domain_origin
                }
                # Try with full browser headers first, fallback to clean session
                resp = requests.get(file_path_or_bytes, headers=headers, timeout=30)
                if resp.status_code != 200:
                    resp = requests.get(file_path_or_bytes, timeout=30)
                if resp.status_code != 200:
                    raise StorageUploadError(f"Failed to download image from URL ({resp.status_code}): {file_path_or_bytes}")
                raw_bytes = resp.content
            else:
                with open(file_path_or_bytes, "rb") as f:
                    raw_bytes = f.read()
        else:
            raw_bytes = file_path_or_bytes

        webp_bytes = self._convert_to_webp(raw_bytes)
        token = str(uuid.uuid4())
        filename = f"{self._random_id(20)}.webp"
        user_uid = self.client.session.uid
        id_token = self.client.session.get_valid_token()
        object_path = f"users/{user_uid}/moments/thumbnails/{filename}"
        encoded_name = urllib.parse.quote(object_path, safe="")

        init_url = f"{self.STORAGE_IMG_URL}/{encoded_name}?uploadType=resumable&name={encoded_name}"
        metadata = {
            "bucket": "",
            "contentType": content_type,
            "name": object_path,
            "metadata": {"visibility": "private", "creator": user_uid},
            "cacheControl": "public, max-age=604800"
        }

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Firebase {id_token}",
            "x-goog-upload-protocol": "resumable",
            "x-goog-upload-command": "start",
            "x-goog-upload-content-type": content_type,
            "x-goog-upload-content-length": str(len(webp_bytes)),
            "x-firebase-storage-version": "ios/12.12.1",
            "x-firebase-gmpid": self.client.session.FIREBASE_APP_ID,
            "User-Agent": f"{self.client.device.user_agent} (GTMSUF/1)"
        }

        init_res = requests.post(init_url, json=metadata, headers=headers)
        if init_res.status_code != 200:
            raise StorageUploadError(f"Image upload initialization failed ({init_res.status_code}): {init_res.text}")

        upload_url = init_res.headers.get("x-goog-upload-url")
        if not upload_url:
            raise StorageUploadError("Missing upload URL from Firebase Storage")

        upload_headers = {
            "Content-Type": "application/octet-stream",
            "x-goog-upload-protocol": "resumable",
            "x-goog-upload-command": "upload, finalize",
            "x-goog-upload-offset": "0",
            "x-goog-upload-content-length": str(len(webp_bytes))
        }

        upload_res = requests.put(upload_url, data=webp_bytes, headers=upload_headers)
        if upload_res.status_code != 200:
            raise StorageUploadError(f"Image upload transfer failed ({upload_res.status_code}): {upload_res.text}")

        download_token = token
        try:
            res_json = upload_res.json()
            if "downloadTokens" in res_json:
                download_token = res_json["downloadTokens"].split(",")[0]
        except Exception:
            pass

        return f"{self.STORAGE_IMG_URL}/{encoded_name}?alt=media&token={download_token}"

    def optimize_video(
        self,
        video_input,
        target_size_bytes: int = 5650000,
        max_dimension: int = 1080,
        preserve_resolution: bool = True,
        priority: str = "balanced",
        progress_callback = None
    ) -> bytes:
        """
        Intelligently compresses and optimizes videos to fit within Locket's 6MB (6,291,455 bytes) limit.
        - priority:
            - 'video' / 'resolution': Allocates highest bitrate to visual resolution.
            - 'audio' / 'music': Prioritizes high audio quality (up to 160-192 kbps AAC) for music/listening.
            - 'balanced' (default): Optimal balance between crystal-clear visuals and solid audio.
        - progress_callback: Optional callable(percent_int, status_text) for real-time progress tracking.
        """
        import os
        import re
        import tempfile
        import subprocess

        # Resolve FFmpeg binary
        ffmpeg_bin = None
        try:
            import imageio_ffmpeg
            ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass

        if not ffmpeg_bin:
            ffmpeg_bin = "ffmpeg"

        temp_in = None
        if isinstance(video_input, bytes):
            fd, temp_in = tempfile.mkstemp(suffix=".mp4")
            with os.fdopen(fd, "wb") as f:
                f.write(video_input)
            in_path = temp_in
        else:
            in_path = video_input

        try:
            # 1. Probe duration, resolution and audio stream
            cmd_probe = [ffmpeg_bin, "-i", in_path]
            p = subprocess.Popen(cmd_probe, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            _, err = p.communicate()
            err_str = err.decode("utf-8", errors="ignore")

            m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", err_str)
            duration = 10.0
            if m:
                h, mins, s = m.groups()
                duration = float(h) * 3600 + float(mins) * 60 + float(s)
                duration = max(1.0, duration)

            has_audio = "Audio:" in err_str

            # 2. Dynamic Bitrate Calculation (Target budget: 5.65 MB safe ceiling)
            total_target_bits = target_size_bytes * 8
            total_bitrate_kbps = (total_target_bits / duration) / 1000

            # PRIORITY HIERARCHY:
            # 1. RESOLUTION (Highest Priority):
            #    Preserve 100% full original resolution (Full HD, 2K, 4K) via Apple HEVC/H.265.
            #    Allocates 80-88% of total bitrate budget directly to visual sharpness.
            # 2. FRAMERATE & MOTION SMOOTHNESS (Second Priority):
            #    - Video < 120s: Preserves original 30/60 FPS for maximum fluidity.
            #    - Video 120s - 300s (2 - 5 mins): Locked at steady 30 FPS.
            #    - Video > 300s (5 - 10 mins): Normalized to 24 FPS (cinema standard) to boost per-frame detail by ~20%.
            #    - Enforces 2-second Keyframe GOP interval (-g = 2*fps) to prevent stream stuttering.
            # 3. AUDIO (Third Priority):
            #    Efficient AAC encoding maintaining clarity while consuming minimal file footprint.

            # Step 1: Audio Bitrate Allocation based on priority
            norm_p = (priority or "balanced").lower()
            if not has_audio:
                audio_kbps = 0
            elif norm_p in ["audio", "music", "tieng", "sound"]:
                # High-fidelity music priority
                if duration > 300:
                    audio_kbps = 64
                elif duration > 120:
                    audio_kbps = 96
                elif duration > 45:
                    audio_kbps = 128
                else:
                    audio_kbps = 160
            elif norm_p in ["video", "resolution", "hinh_anh"]:
                # Video sharpness priority
                if duration > 300:
                    audio_kbps = 24
                elif duration > 120:
                    audio_kbps = 32
                elif duration > 45:
                    audio_kbps = 48
                else:
                    audio_kbps = 64
            else:
                # Balanced (default)
                if duration > 300:
                    audio_kbps = 32
                elif duration > 120:
                    audio_kbps = 64
                elif duration > 45:
                    audio_kbps = 96
                else:
                    audio_kbps = 128

            # Step 2: Framing & FPS Selection
            if duration > 300:
                fps_target = 24  # Cinema standard boosts per-frame sharpness for ultra-long clips
                mux_overhead = 0.88
            elif duration > 120:
                fps_target = 30  # Smooth 30 FPS
                mux_overhead = 0.91
            else:
                fps_target = None  # Preserve original video framerate
                mux_overhead = 0.94

            gop_size = (fps_target or 30) * 2

            # Step 3: Visual Resolution Bitrate Allocation
            net_bitrate_kbps = total_bitrate_kbps * mux_overhead
            video_kbps = int(net_bitrate_kbps - audio_kbps)
            video_kbps = max(35, min(video_kbps, 4000))

            fd_out, temp_out = tempfile.mkstemp(suffix=".mp4")
            os.close(fd_out)

            # Check if FFmpeg has libx265 (HEVC) available for ultra-high efficiency while keeping 100% resolution
            use_hevc = False
            if preserve_resolution:
                try:
                    chk = subprocess.run([ffmpeg_bin, "-encoders"], capture_output=True, text=True)
                    if "libx265" in chk.stdout:
                        use_hevc = True
                except Exception:
                    pass

            # Choose preset: use 'veryfast' for very long clips (>180s) to encode quickly without timeout
            enc_preset = "veryfast" if duration > 180 else "fast"

            if use_hevc:
                # H.265 / HEVC: Keeps 100% original resolution with Apple 'hvc1' tag, halving file size
                scale_filter = "scale=trunc(iw/2)*2:trunc(ih/2)*2"
                cmd_compress = [
                    ffmpeg_bin, "-y",
                    "-i", in_path,
                    "-c:v", "libx265",
                    "-tag:v", "hvc1",
                    "-pix_fmt", "yuv420p",
                    "-preset", enc_preset,
                    "-b:v", f"{video_kbps}k",
                    "-maxrate", f"{video_kbps}k",
                    "-bufsize", f"{int(video_kbps * 1.2)}k",
                    "-g", str(gop_size),
                    "-keyint_min", str(gop_size // 2),
                    "-x265-params", f"no-open-gop=1:repeat-headers=1",
                    "-vf", scale_filter,
                    "-movflags", "+faststart"
                ]
                if fps_target:
                    cmd_compress.extend(["-r", str(fps_target)])
            else:
                # H.264 standard
                if preserve_resolution:
                    scale_filter = "scale=trunc(iw/2)*2:trunc(ih/2)*2"
                else:
                    scale_limit = 720 if duration > 45 else max_dimension
                    scale_filter = (
                        f"scale=w='min({scale_limit},iw)':h='min({scale_limit},ih)':force_original_aspect_ratio=decrease,"
                        f"scale=trunc(iw/2)*2:trunc(ih/2)*2"
                    )

                cmd_compress = [
                    ffmpeg_bin, "-y",
                    "-i", in_path,
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-preset", "fast",
                    "-b:v", f"{video_kbps}k",
                    "-maxrate", f"{int(video_kbps * 1.15)}k",
                    "-bufsize", f"{int(video_kbps * 1.8)}k",
                    "-g", str(gop_size),
                    "-keyint_min", str(gop_size // 2),
                    "-vf", scale_filter,
                    "-movflags", "+faststart"
                ]
                if fps_target:
                    cmd_compress.extend(["-r", str(fps_target)])

            if has_audio:
                cmd_compress.extend(["-c:a", "aac", "-b:a", f"{audio_kbps}k"])
            else:
                cmd_compress.extend(["-an"])

            cmd_compress.append(temp_out)

            # Run FFmpeg with real-time progress parsing
            proc = subprocess.Popen(
                cmd_compress,
                stderr=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                universal_newlines=True,
                encoding="utf-8",
                errors="ignore"
            )

            time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")
            last_pct = -1
            while True:
                line = proc.stderr.readline()
                if not line and proc.poll() is not None:
                    break
                if line:
                    match = time_pattern.search(line)
                    if match:
                        cur_h, cur_m, cur_s = match.groups()
                        cur_sec = float(cur_h) * 3600 + float(cur_m) * 60 + float(cur_s)
                        pct = min(99, int((cur_sec / duration) * 100))
                        if pct != last_pct:
                            last_pct = pct
                            if progress_callback:
                                try:
                                    progress_callback(pct, f"Nén video HEVC ({pct}%)...")
                                except Exception:
                                    pass

            retcode = proc.wait()
            if retcode != 0:
                raise StorageUploadError("Video compression failed during encoding.")

            if progress_callback:
                try:
                    progress_callback(100, "Nén video hoàn tất 100%!")
                except Exception:
                    pass

            with open(temp_out, "rb") as f:
                out_bytes = f.read()

            os.remove(temp_out)
            return out_bytes
        finally:
            if temp_in and os.path.exists(temp_in):
                try:
                    os.remove(temp_in)
                except Exception:
                    pass

    def upload_video(
        self,
        video_path_or_bytes,
        content_type: str = "video/mp4",
        auto_compress: bool = True,
        priority: str = "balanced",
        progress_callback = None
    ) -> str:
        """
        Uploads a video to Locket Video Storage using Google Resumable Upload protocol.
        Automatically checks size and compresses video if >= 6 MB (6,291,455 bytes) when auto_compress=True.
        - priority: 'video' (visual sharpness), 'audio' (music/sound), or 'balanced'.
        - progress_callback: Optional callable(percent_int, status_text) for tracking.
        """
        import requests
        if isinstance(video_path_or_bytes, str):
            if video_path_or_bytes.startswith("http://") or video_path_or_bytes.startswith("https://"):
                parsed_vurl = urllib.parse.urlparse(video_path_or_bytes)
                v_origin = f"{parsed_vurl.scheme}://{parsed_vurl.netloc}/"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Referer": v_origin
                }
                resp = requests.get(video_path_or_bytes, headers=headers, timeout=120)
                if resp.status_code != 200:
                    resp = requests.get(video_path_or_bytes, timeout=120)
                if resp.status_code != 200:
                    raise StorageUploadError(f"Failed to download video from URL ({resp.status_code}): {video_path_or_bytes}")
                video_bytes = resp.content
                video_input = video_bytes
            else:
                with open(video_path_or_bytes, "rb") as f:
                    video_bytes = f.read()
                video_input = video_path_or_bytes
        else:
            video_bytes = video_path_or_bytes
            video_input = video_bytes

        # Automatic compression if video exceeds or approaches Locket's 6MB ceiling
        if len(video_bytes) >= 6291456:
            if auto_compress:
                video_bytes = self.optimize_video(
                    video_input,
                    priority=priority,
                    progress_callback=progress_callback
                )
            else:
                raise StorageUploadError(
                    f"Video size ({len(video_bytes)} bytes / {len(video_bytes)/1024/1024:.2f} MB) exceeds "
                    "Locket's strict limit of 6 MB (6,291,455 bytes). Please compress before uploading."
                )

        token = str(uuid.uuid4())
        filename = f"{self._random_id(20)}.mp4"
        user_uid = self.client.session.uid
        id_token = self.client.session.get_valid_token()
        object_path = f"users/{user_uid}/moments/videos/{filename}"
        encoded_name = urllib.parse.quote(object_path, safe="")
        init_url = f"{self.STORAGE_VIDEO_URL}/{encoded_name}?uploadType=resumable&name={encoded_name}"
        metadata = {
            "bucket": "",
            "contentType": content_type,
            "name": object_path,
            "metadata": {"visibility": "private", "creator": user_uid},
            "cacheControl": "public, max-age=604800"
        }

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Firebase {id_token}",
            "x-goog-upload-protocol": "resumable",
            "x-goog-upload-command": "start",
            "x-goog-upload-content-type": content_type,
            "x-goog-upload-content-length": str(len(video_bytes)),
            "x-firebase-storage-version": "ios/12.12.1",
            "x-firebase-gmpid": self.client.session.FIREBASE_APP_ID,
            "User-Agent": f"{self.client.device.user_agent} (GTMSUF/1)"
        }

        init_res = requests.post(init_url, json=metadata, headers=headers)
        if init_res.status_code != 200:
            raise StorageUploadError(f"Video upload initialization failed ({init_res.status_code}): {init_res.text}")

        upload_url = init_res.headers.get("x-goog-upload-url")
        if not upload_url:
            raise StorageUploadError("Missing upload URL from Firebase Storage")

        upload_headers = {
            "Content-Type": "application/octet-stream",
            "x-goog-upload-protocol": "resumable",
            "x-goog-upload-command": "upload, finalize",
            "x-goog-upload-offset": "0",
            "x-goog-upload-content-length": str(len(video_bytes))
        }

        upload_res = requests.put(upload_url, data=video_bytes, headers=upload_headers)
        if upload_res.status_code != 200:
            raise StorageUploadError(f"Video data upload failed ({upload_res.status_code}): {upload_res.text}")

        download_token = token
        try:
            res_json = upload_res.json()
            if "downloadTokens" in res_json:
                download_token = res_json["downloadTokens"].split(",")[0]
        except Exception:
            pass

        return f"{self.STORAGE_VIDEO_URL}/{encoded_name}?alt=media&token={download_token}"

    def build_overlay(
        self,
        text: str = "",
        note_type: str = NoteType.STANDARD,
        icon: str = None,
        colors: list = None,
        text_color: str = None
    ) -> dict:
        """
        Constructs rich Locket caption/note overlay payload.
        Automatically injects authentic background colors and emoji icons for preset badges.
        """
        import os
        import json

        # Check if note_type matches an official preset
        preset_info = None
        preset_file = os.path.join(os.path.dirname(__file__), "..", "caption_presets.json")
        clean_key = note_type.replace("caption:", "")
        if os.path.exists(preset_file):
            try:
                with open(preset_file, "r", encoding="utf-8") as pf:
                    presets = json.load(pf)
                    preset_info = presets.get(clean_key)
            except Exception:
                pass

        final_text = text
        final_type = note_type
        final_colors = colors if colors is not None else []
        final_text_color = text_color or "#FFFFFFE6"
        final_icon = icon

        if preset_info:
            if not final_text:
                final_text = preset_info.get("text", "")
            final_type = preset_info.get("type", "static_content")
            if colors is None:
                final_colors = preset_info.get("colors", [])
            if not text_color and "text_color" in preset_info:
                final_text_color = preset_info["text_color"]
            if not final_icon and preset_info.get("icon"):
                final_icon = preset_info["icon"]

        # Determine genuine overlay_id
        if note_type == NoteType.STANDARD:
            target_overlay_id = "caption:standard"
            data_type = "standard"
        elif preset_info and preset_info.get("overlay_id"):
            target_overlay_id = preset_info["overlay_id"]
            data_type = preset_info.get("type", "static_content")
        elif note_type.startswith("caption:"):
            target_overlay_id = note_type
            data_type = "static_content" if "static_content" in final_type else note_type.split(":")[-1]
        else:
            target_overlay_id = f"caption:{note_type}"
            data_type = note_type

        # Build genuine data structure
        max_lines_val = "1" if (preset_info or data_type in ["static_content", "streak", "time", "review"]) else "4"
        overlay_data = {
            "text": final_text,
            "type": data_type,
            "text_color": final_text_color,
            "max_lines": {
                "value": max_lines_val,
                "@type": "type.googleapis.com/google.protobuf.Int64Value"
            },
            "background": {
                "material_blur": "ultra_thin" if not final_colors else "regular",
                "colors": final_colors
            }
        }
        if final_icon:
            overlay_data["icon"] = {
                "data": final_icon,
                "type": "emoji"
            }

        return {
            "overlay_type": "caption",
            "overlay_id": target_overlay_id,
            "alt_text": f"{final_icon} {final_text}" if final_icon else final_text,
            "data": overlay_data
        }

    def post(
        self,
        image = None,
        caption: str = "",
        video = None,
        note_type: str = NoteType.STANDARD,
        icon: str = None,
        colors: list = None,
        text_color: str = None,
        is_private: bool = False,
        recipients: list = None,
        auto_compress: bool = True,
        priority: str = "balanced",
        progress_callback = None
    ) -> dict:
        """
        Posts a new moment photo or video to Locket.
        - image: Image file path, raw bytes, or pre-uploaded image URL (serves as thumbnail for videos. If None, auto-extracted from video).
        - caption: Text note displayed on the moment (if empty and using a badge preset, uses default preset text).
        - video: Optional video file path, raw bytes, or pre-uploaded video URL.
        - note_type: Style of the note (standard, NoteType.IN_LOVE_LONGING, NoteType.PARTY_TIME, etc.).
        - icon: Optional emoji icon inside the colored pill badge.
        - colors: Optional list of hex colors for the pill badge gradient (e.g. ['#FF5F6D', '#FFC371']).
        - text_color: Optional text color hex code (e.g. '#FFFFFF', '#000000').
        - is_private: Set to True to send only to yourself.
        - recipients: List of specific friend UIDs (leave empty/None to broadcast to all friends).
        - auto_compress: Automatically compress video if size >= 6MB (default True).
        - priority: Video compression priority ('video', 'audio'/'music', or 'balanced').
        - progress_callback: Optional callable(percent_int, status_text) for encoding progress.
        """
        # If posting a video without a dedicated thumbnail, auto-extract high quality frame
        if video and not image:
            image = self.extract_thumbnail(video)

        if isinstance(image, str) and (image.startswith("http://") or image.startswith("https://")):
            if "firebasestorage.googleapis.com" in image and "alt=media" in image:
                thumb_url = image
            else:
                thumb_url = self.upload_image(image)
        elif image:
            thumb_url = self.upload_image(image)
        else:
            thumb_url = ""

        video_url = None
        if video:
            if isinstance(video, str) and (video.startswith("http://") or video.startswith("https://")):
                # If already a valid Locket Firebase Storage video URL, use directly
                if "firebasestorage.googleapis.com" in video and "alt=media" in video:
                    video_url = video
                else:
                    # External video URL (TikTok, Youtube, CDN, etc.): upload to Locket Storage
                    video_url = self.upload_video(
                        video,
                        auto_compress=auto_compress,
                        priority=priority,
                        progress_callback=progress_callback
                    )
            else:
                video_url = self.upload_video(
                    video,
                    auto_compress=auto_compress,
                    priority=priority,
                    progress_callback=progress_callback
                )

        overlays = []
        if caption or note_type != NoteType.STANDARD or colors or icon:
            ov = self.build_overlay(text=caption, note_type=note_type, icon=icon, colors=colors, text_color=text_color)
            overlays.append(ov)
            if not caption:
                caption = ov.get("alt_text", "")

        payload = {
            "thumbnail_url": thumb_url,
            "overlays": overlays,
            "sent_to_self_only": is_private,
            "sent_to_all": not is_private and not recipients,
            "recipients": recipients or [],
            "md5": f"{uuid.uuid4().hex}_{int(time.time())}"
        }
        if caption and not overlays:
            payload["caption"] = caption
        if video_url:
            payload["video_url"] = video_url

        res = self.client.post_api("postMomentV2", payload)
        if isinstance(res, dict) and (res.get("status") not in (200, None) or "errors" in res):
            err_msg = res.get("errors") or res.get("error") or f"Locket API error {res.get('status')}"
            raise LocketAPIError(f"Post moment failed: {err_msg}")

        data_res = res.get("data", res)
        if isinstance(data_res, dict):
            if "id" not in data_res and "canonical_uid" in data_res:
                data_res["id"] = data_res["canonical_uid"]
            # Save to posted moments history
            moment_entry = {
                "moment_uid": data_res.get("canonical_uid") or data_res.get("id"),
                "canonical_uid": data_res.get("canonical_uid") or data_res.get("id"),
                "thumbnail_url": thumb_url,
                "video_url": video_url,
                "caption": caption or "",
                "created_at": datetime.utcnow().isoformat() + "Z" if "datetime" in globals() else str(int(time.time()))
            }
            self.record_posted_moment(moment_entry)
        return data_res

    def get_latest(self) -> list:
        """Fetches the latest moments feed from your friends."""
        res = self.client.post_api("getLatestMomentV2", {"should_count_missed_moments": True})
        return res.get("data", [])

    def get_shared_moments_by_username(self, username: str, limit: int = None) -> list:
        """
        Retrieves actual posted moments (photos/videos) from a specific user's feed.
        - username: Target username (e.g. 'friend_username').
        - limit: Maximum number of recent moments to retrieve.
        """
        profile = self.client.user.get_profile_by_username(username)
        target_uid = profile.get("uid")
        if not target_uid:
            return []
        return self.get_shared_moments_by_user(target_uid, limit=limit)

    def get_shared_moments_by_user(self, user_uid: str, limit: int = None) -> list:
        """
        Retrieves actual posted moments (photos/videos) from a user UID via Locket feed API.
        Traverses feed history using sync_token pagination to fetch all available moments.
        Returns authentic moment objects with complete metadata (overlays, thumbnails, caption, timestamps).
        """
        moments = []
        seen_uids = set()
        current_sync = None

        try:
            all_friends = self.client.friends.get_all_friends()
            friend_uids = [f.get("uid") for f in all_friends if f.get("uid")]
            other_friends = [fuid for fuid in friend_uids if fuid != user_uid]

            while True:
                payload = {
                    "should_count_missed_moments": True,
                    "include_group_moments": True,
                    "excluded_users": other_friends
                }
                if current_sync:
                    payload["sync_token"] = current_sync

                feed_res = self.client.post_api("getLatestMomentV2", payload)
                data = feed_res.get("data", [])
                if not data:
                    break

                new_count = 0
                for m in data:
                    mid = m.get("canonical_uid")
                    if mid and mid not in seen_uids:
                        seen_uids.add(mid)
                        new_count += 1
                        current_sync = mid
                        if m.get("user") == user_uid:
                            created_ts = ""
                            date_field = m.get("date", {})
                            if isinstance(date_field, dict) and "_seconds" in date_field:
                                created_ts = str(date_field["_seconds"])
                            moments.append({
                                "moment_uid": mid,
                                "user_uid": user_uid,
                                "thumbnail_url": m.get("thumbnail_url"),
                                "image_url": m.get("image_url") or m.get("thumbnail_url"),
                                "video_url": m.get("video_url"),
                                "caption": m.get("caption", ""),
                                "overlays": m.get("overlays", []),
                                "created_at": created_ts,
                                "date": date_field,
                                "md5": m.get("md5"),
                                "source": "feed"
                            })
                            if limit and len(moments) >= limit:
                                return moments[:limit]

                if new_count == 0 or feed_res.get("status") == 304:
                    break
        except Exception:
            pass

        return moments

    # Backward compatibility alias
    get_posts_by_username = get_shared_moments_by_username
    get_posts_by_user = get_shared_moments_by_user

    def get_filters(self) -> dict:
        """Fetches available camera filters."""
        res = self.client.post_api("getFilters", {})
        return res.get("data", res)

    def mark_as_viewed(self, moment_uid: str) -> dict:
        """Marks a moment as viewed."""
        res = self.client.post_api("markMomentAsViewed", {"moment_uid": moment_uid})
        return res

    def react(self, moment_uid: str, reaction: str = "❤️", from_memory: bool = False) -> dict:
        """
        Sends an emoji reaction to a photo or video moment on Locket.
        - moment_uid: The unique ID of the target moment.
        - reaction: Emoji character (e.g. '😍', '❤️', '🔥', '😂').
        - from_memory: Whether the moment is viewed from past memory recap.
        """
        payload = {
            "moment_uid": moment_uid,
            "reaction": reaction,
            "from_memory": from_memory,
            "intensity": {
                "@type": "type.googleapis.com/google.protobuf.Int64Value",
                "value": "0"
            }
        }
        res = self.client.post_api("reactToMoment", payload)
        return res

    def get_rollcall_posts(self, week_of_year: int = None, year: int = None, source: str = "banner") -> dict:
        """
        Fetches weekly Rollcall posts.
        - week_of_year: ISO calendar week number (defaults to current week).
        - year: Calendar year (defaults to current year).
        - source: 'banner' or 'feed' (defaults to 'banner').
        """
        import datetime
        now = datetime.date.today()
        iso_year, iso_week, _ = now.isocalendar()
        if week_of_year is None:
            week_of_year = iso_week
        if year is None:
            year = iso_year

        payload = {
            "week_of_year": {
                "@type": "type.googleapis.com/google.protobuf.Int64Value",
                "value": str(week_of_year)
            },
            "year": {
                "@type": "type.googleapis.com/google.protobuf.Int64Value",
                "value": str(year)
            },
            "source": source
        }
        res = self.client.post_api("getRollcallPosts", payload)
        return res.get("data", res)

    def get_all_my_moments(
        self,
        limit: int = None,
        start_date: str = None,
        end_date: str = None
    ) -> list:
        """
        Retrieves moments posted by the current authenticated account (bot),
        complete with their views count, viewers list, and emoji reactions.

        Parameters:
        - limit: (int, optional) Number of most recent moments to return. If None, returns all matching moments.
        - start_date: (str, optional) Filter moments created on or after this date/timestamp (ISO-8601 string e.g. '2026-10-14' or '2026-10-14T00:00:00Z').
        - end_date: (str, optional) Filter moments created on or before this date/timestamp (ISO-8601 string e.g. '2026-10-15' or '2026-10-14T23:59:59Z').

        Returns:
            list of dicts containing moment_uid, thumbnail_url, views_count, viewers, reactions, and created_at.
        """
        import json
        import urllib.request
        from datetime import datetime

        def parse_ts(ts_str):
            if not ts_str:
                return None
            try:
                # Handle formats like 2026-10-14T08:08:31.822Z or 2026-10-14
                s = str(ts_str).replace("Z", "+00:00")
                if len(s) == 10:  # YYYY-MM-DD
                    s += "T00:00:00+00:00"
                return datetime.fromisoformat(s)
            except Exception:
                return None

        dt_start = parse_ts(start_date)
        dt_end = parse_ts(end_date)
        if dt_end and len(str(end_date).strip()) == 10:
            # If date given as 'YYYY-MM-DD', treat end_date as end of day
            dt_end = dt_end.replace(hour=23, minute=59, second=59, microsecond=999999)

        token = self.client.session.get_valid_token()
        my_uid = self.client.session.uid
        moments = []
        seen_mids = set()

        # 1. First, retrieve actual posted moments from local history (posted via client.moments.post)
        posted_history = self._load_history()
        for p in posted_history:
            mid = p.get("moment_uid") or p.get("canonical_uid") or p.get("id")
            if not mid or mid in seen_mids:
                continue

            created_at_raw = p.get("created_at", "")
            if dt_start or dt_end:
                doc_dt = parse_ts(created_at_raw)
                if doc_dt:
                    if dt_start and doc_dt < dt_start:
                        continue
                    if dt_end and doc_dt > dt_end:
                        continue

            seen_mids.add(mid)
            views_data = self.get_views(mid)
            moments.append({
                "moment_uid": mid,
                "thumbnail_url": p.get("thumbnail_url"),
                "video_url": p.get("video_url"),
                "caption": p.get("caption", ""),
                "views_count": views_data.get("count", 0),
                "viewers": views_data.get("moment_views", []),
                "reactions": views_data.get("reactions", []),
                "created_at": created_at_raw,
                "source": "posted_moment"
            })
            if limit and len(moments) >= limit:
                return moments[:limit]

        # 2. Discover authentic posted moments from account conversations
        # In Locket, whenever you post a moment, it is shared with friends or in groups.
        # We identify our moments by inspecting the thumbnail_url path (users/<my_uid>/moments/thumbnails/...)
        try:
            u_url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/users/{my_uid}/conversations"
            req = urllib.request.Request(u_url, headers={"Authorization": f"Bearer {token}"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                udata = json.loads(resp.read().decode("utf-8"))

            user_storage_path = f"users%2F{my_uid}%2Fmoments"

            for doc in udata.get("documents", []):
                cid = doc["name"].split("/")[-1]
                m_url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/conversations/{cid}/messages?pageSize=200"
                m_req = urllib.request.Request(m_url, headers={"Authorization": f"Bearer {token}"})
                with urllib.request.urlopen(m_req, timeout=10) as m_resp:
                    m_data = json.loads(m_resp.read().decode("utf-8"))

                for mdoc in m_data.get("documents", []):
                    f = mdoc.get("fields", {})
                    thumb = f.get("thumbnail_url", {}).get("stringValue", "")
                    rm = f.get("reply_moment", {}).get("stringValue")
                    created_at_raw = f.get("created_at", {}).get("timestampValue", "")

                    # Verify that this media was created and uploaded by current user
                    if thumb and user_storage_path in thumb:
                        mid = rm or mdoc["name"].split("/")[-1]
                        if not mid or mid in seen_mids:
                            continue

                        # Check date filter
                        if dt_start or dt_end:
                            doc_dt = parse_ts(created_at_raw)
                            if doc_dt:
                                if dt_start and doc_dt < dt_start:
                                    continue
                                if dt_end and doc_dt > dt_end:
                                    continue

                        # Fetch authentic views and reactions
                        views_data = self.get_views(mid)
                        # An authentic moment of our user will return 200 or have views/reactions
                        if views_data.get("status") in (200, None) or "count" in views_data:
                            seen_mids.add(mid)
                            moments.append({
                                "moment_uid": mid,
                                "thumbnail_url": thumb,
                                "video_url": None,
                                "caption": "",
                                "views_count": views_data.get("count", 0),
                                "viewers": views_data.get("moment_views", []),
                                "reactions": views_data.get("reactions", []),
                                "created_at": created_at_raw,
                                "source": "posted_moment"
                            })
                            if limit and len(moments) >= limit:
                                return moments[:limit]
        except Exception:
            pass

        return moments

    def get_views(self, moment_uid: str) -> dict:
        """
        Fetches the views count, list of viewers, and any emoji reactions on this moment.
        - moment_uid: The unique ID of the moment.
        Returns:
            dict containing:
              - count: int (number of views)
              - moment_views: list of viewers with viewed_at timestamps
              - reactions: list of emoji reactions with sender and created_at timestamps
        """
        import json
        import urllib.request

        payload = {"moment_uid": moment_uid}
        res = self.client.post_api("getMomentViews", payload)
        views_dict = res.get("data", res) if isinstance(res, dict) else {}

        # Fetch authentic moment reactions from Firestore moments/{mid}/reactions
        reactions = []
        try:
            token = self.client.session.get_valid_token()
            url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/moments/{moment_uid}/reactions"
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for doc in data.get("documents", []):
                    f = doc.get("fields", {})
                    reactions.append({
                        "emoji": f.get("string", {}).get("stringValue", ""),
                        "sender": f.get("user", {}).get("stringValue", ""),
                        "created_at": f.get("created_at", {}).get("timestampValue", "")
                    })
        except Exception:
            pass

        if isinstance(views_dict, dict):
            views_dict["reactions"] = reactions
        return views_dict

    def comment(self, moment_uid: str, receiver_uid: str, text: str, from_memory: bool = False) -> dict:
        """
        Sends a comment on a moment (this creates/appends a chat message linked to the moment).
        - moment_uid: Target moment ID.
        - receiver_uid: The author's UID of the moment.
        - text: Comment message content.
        - from_memory: Whether the moment is from memories.
        """
        payload = {
            "moment_uid": moment_uid,
            "receiver_uid": receiver_uid,
            "msg": text,
            "from_memory": from_memory,
            "client_token": None
        }
        res = self.client.post_api("sendChatMessageV2", payload)
        return res.get("data", res)

    def delete(self, moment_uid: str) -> dict:
        """Deletes a posted moment."""
        res = self.client.post_api("deleteMomentV2", {
            "moment_uid": moment_uid,
            "canonical_uid": moment_uid
        })
        return res
