// ============================================================
// Locket Profile & Badge Keeper - LAMDev
// Website: https://dalymmo.com
// Channel: https://t.me/dalymmocom
// Chức năng: Giữ Huy hiệu Gold luôn BẬT vĩnh viễn không bị văng/mất
// ============================================================

const url = $request.url;

// 1. KHI BẬT CÔNG TẮC HUY HIỆU (changeProfileInfo):
// Mock phản hồi HTTP 200 OK ngay lập tức, không để Google Server từ chối
if (url.includes("changeProfileInfo")) {
    $done({
        response: {
            status: 200,
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({
                result: {
                    badge: "locket_gold",
                    success: true
                }
            })
        }
    });
} else {
    // 2. KHI TẢI DỮ LIỆU USER (fetchUser / fetchUserV2 / fetchUsers):
    // Đảm bảo thông tin user luôn mang huy hiệu "locket_gold"
    let body = $response ? $response.body : null;
    
    if (body) {
        try {
            let obj = JSON.parse(body);
            if (obj && obj.result) {
                if (Array.isArray(obj.result)) {
                    obj.result.forEach(u => {
                        if (u && typeof u === "object") {
                            u.badge = "locket_gold";
                        }
                    });
                } else if (typeof obj.result === "object") {
                    obj.result.badge = "locket_gold";
                }
            }
            body = JSON.stringify(obj);
        } catch (e) {
            // Giữ nguyên body nếu không parse được JSON
        }
    }
    
    $done({ body });
}
