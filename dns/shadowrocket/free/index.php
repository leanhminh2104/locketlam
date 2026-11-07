<?php
/**
 * ==============================================================================
 * GÓI LOCKET FREE DO LAMDEV x DALYMMO.COM PHÁT HÀNH
 * Máy chủ DNS-over-HTTPS (DoH) độc quyền - Chuẩn RFC 8484
 * Chống thu hồi chứng chỉ Apple vĩnh viễn & Giữ Locket Gold VIP không giới hạn
 * 
 * 🌐 Website: https://dalymmo.com
 * 🛠 Phát hành bởi: LAMDev x DaLyMMO.com
 * 📦 Endpoint: lamdev.unaux.com/locketlam/dns/shadowrocket/free
 * ==============================================================================
 */

// Bật đầy đủ CORS headers cho iOS và các client DoH
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept, X-Requested-With');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// 🛡️ DANH SÁCH DOMAIN CHẶN (Sinkhole 0.0.0.0 / ::)
$blockedDomains = [
    // 1. Chống thu hồi chứng chỉ Apple (ESign, Scarlet, GBox, TrollStore, IPA Doanh Nghiệp)
    'certs.apple.com',
    'certs.apple.com.edgekey.net',
    'crl.apple.com',
    'crl.apple.com.akadns.net',
    'crl.apple.com.edgekey.net',
    'crl.entrust.net',
    'crl3.digicert.com',
    'crl4.digicert.com',
    'ocsp-lb.apple.com.akadns.net',
    'ocsp.apple.com',
    'ocsp.apple.com.edgekey.net',
    'ocsp.digicert.cn',
    'ocsp.digicert.com',
    'ocsp2.apple.com',
    'ocsp2.apple.com.edgekey.net',
    'valid.apple.com',
    'valid.apple.com.akadns.net',
    'valid.apple.com.edgekey.net',
    'ppq.apple.com',
    'iadsdk.apple.com',

    // 2. Chống thu hồi Locket Gold Free VIP (RevenueCat, Backup & Tracking)
    'api.revenuecat.com',
    'app.revenuecat.com',
    'api.rc-backup.com',
    'in.appcenter.ms',
    'app-measurement.com',
    'firebaselogging-pa.googleapis.com',
    'mixpanel.com',
    'api.mixpanel.com'
];

// Nhận dữ liệu DNS Query (hỗ trợ cả POST và GET base64url theo chuẩn RFC 8484)
$dnsQuery = '';
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (!empty($_GET['dns'])) {
        $base64 = strtr($_GET['dns'], '-_', '+/');
        $pad = strlen($base64) % 4;
        if ($pad > 0) {
            $base64 .= str_repeat('=', 4 - $pad);
        }
        $dnsQuery = base64_decode($base64);
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $dnsQuery = file_get_contents('php://input');
}

// Nếu truy cập từ trình duyệt Web -> Hiện Dashboard kiểm tra trạng thái
if (empty($dnsQuery) || strlen($dnsQuery) < 12) {
    header('Content-Type: text/html; charset=utf-8');
    ?>
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gói Locket Free - LAMDev x DaLyMMO.com</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; }
            body { background: #0b0f19; color: #f3f4f6; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
            .container { background: #111827; border: 1px solid #1f2937; border-radius: 20px; padding: 36px 30px; max-width: 580px; width: 100%; box-shadow: 0 20px 50px rgba(0,0,0,0.6); position: relative; overflow: hidden; }
            .container::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #f59e0b, #ef4444, #8b5cf6, #3b82f6); }
            .badge-live { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(34, 197, 94, 0.12); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 9999px; font-size: 13px; font-weight: 600; margin-bottom: 20px; }
            .badge-live::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 12px #22c55e; }
            h1 { font-size: 24px; font-weight: 800; color: #f59e0b; margin-bottom: 8px; line-height: 1.3; }
            .author { font-size: 14px; font-weight: 600; color: #9ca3af; margin-bottom: 20px; }
            .author span { color: #38bdf8; }
            p { font-size: 14px; line-height: 1.6; color: #9ca3af; margin-bottom: 24px; }
            .info-grid { display: grid; grid-template-columns: 1fr; gap: 10px; margin-bottom: 24px; }
            .info-item { background: #1a2234; border: 1px solid #28334e; border-radius: 12px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; }
            .info-item .title { font-size: 13px; color: #94a3b8; }
            .info-item .value { font-size: 13px; font-weight: 700; color: #f8fafc; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
            .btn-group { display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px; }
            .btn { display: inline-block; text-align: center; padding: 14px 20px; border-radius: 12px; font-size: 14px; font-weight: 700; text-decoration: none; transition: 0.2s ease; cursor: pointer; }
            .btn-primary { background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3); }
            .btn-primary:hover { filter: brightness(1.1); transform: translateY(-1px); }
            .footer { border-top: 1px solid #1f2937; padding-top: 20px; font-size: 12px; color: #6b7280; text-align: center; }
            .footer a { color: #f59e0b; text-decoration: none; font-weight: 600; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="badge-live">DNS-over-HTTPS Online (RFC 8484)</div>
            <h1>💛 Gói Locket Free</h1>
            <div class="author">Phát hành độc quyền bởi: <span>LAMDev x DaLyMMO.com</span></div>
            <p>Hệ thống máy chủ DoH tốc độ cao, hoạt động 100% không giới hạn truy vấn, tự động chặn toàn bộ yêu cầu thu hồi chứng chỉ Apple và xác thực Locket Gold.</p>
            
            <div class="info-grid">
                <div class="info-item">
                    <span class="title">Trạng thái:</span>
                    <span class="value" style="color: #4ade80;">Active / 100% Ready</span>
                </div>
                <div class="info-item">
                    <span class="title">Giao thức:</span>
                    <span class="value">DoH (RFC 8484)</span>
                </div>
                <div class="info-item">
                    <span class="title">Cơ chế bảo vệ:</span>
                    <span class="value">Sinkhole (0.0.0.0 / ::)</span>
                </div>
                <div class="info-item">
                    <span class="title">Upstream DNS:</span>
                    <span class="value">Cloudflare (1.1.1.1)</span>
                </div>
                <div class="info-item">
                    <span class="title">Giới hạn truy vấn:</span>
                    <span class="value" style="color: #f59e0b;">Không giới hạn (Unlimited)</span>
                </div>
            </div>

            <div class="btn-group">
                <a href="https://dalymmo.com" target="_blank" class="btn btn-primary">🌐 Ghé thăm Website DaLyMMO.com</a>
            </div>

            <div class="footer">
                &copy; <?= date('Y') ?> <strong>Gói Locket Free do LAMDev x DaLyMMO.com phát hành</strong>. Tất cả quyền được bảo lưu.
            </div>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// ------------------------------------------------------------------------------
// XỬ LÝ TRUY VẤN DNS-OVER-HTTPS (RFC 8484)
// ------------------------------------------------------------------------------
$txId = substr($dnsQuery, 0, 2);
$offset = 12;
$domainParts = [];
$len = strlen($dnsQuery);

while ($offset < $len) {
    $labelLen = ord($dnsQuery[$offset]);
    if ($labelLen === 0) {
        $offset++;
        break;
    }
    $offset++;
    if ($offset + $labelLen > $len) break;
    $domainParts[] = substr($dnsQuery, $offset, $labelLen);
    $offset += $labelLen;
}

$queryDomain = strtolower(implode('.', $domainParts));
$qType = 0;
$qSection = '';

if ($offset + 4 <= $len) {
    $qType = (ord($dnsQuery[$offset]) << 8) | ord($dnsQuery[$offset + 1]);
    $qSection = substr($dnsQuery, 12, ($offset + 4) - 12);
}

// Kiểm tra danh sách chặn
$isBlocked = false;
foreach ($blockedDomains as $bDomain) {
    if ($queryDomain === $bDomain || str_ends_with($queryDomain, '.' . $bDomain)) {
        $isBlocked = true;
        break;
    }
}

header('Content-Type: application/dns-message');
header('Cache-Control: public, max-age=300');

if ($isBlocked && !empty($qSection)) {
    // Trả về kết quả Sinkhole chặn hoàn toàn (QR=1, RD=1, RA=1, RCODE=0 NOERROR)
    $respFlags = "\x81\x80";
    
    if ($qType === 1) { // Type A: 0.0.0.0
        $header = $txId . $respFlags . "\x00\x01\x00\x01\x00\x00\x00\x00";
        $answer = "\xc0\x0c\x00\x01\x00\x01\x00\x00\x01\x2c\x00\x04\x00\x00\x00\x00";
        echo $header . $qSection . $answer;
        exit;
    } elseif ($qType === 28) { // Type AAAA: ::
        $header = $txId . $respFlags . "\x00\x01\x00\x01\x00\x00\x00\x00";
        $answer = "\xc0\x0c\x00\x1c\x00\x01\x00\x00\x01\x2c\x00\x10" . str_repeat("\x00", 16);
        echo $header . $qSection . $answer;
        exit;
    } else { // Các loại khác (HTTPS, TXT, NODATA)
        $header = $txId . $respFlags . "\x00\x01\x00\x00\x00\x00\x00\x00";
        echo $header . $qSection;
        exit;
    }
}

// Chuyển tiếp tên miền thông thường tới Upstream DoH (Cloudflare 1.1.1.1)
$upstreamUrl = 'https://1.1.1.1/dns-query';
if (function_exists('curl_init')) {
    $ch = curl_init($upstreamUrl);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $dnsQuery);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/dns-message',
        'Accept: application/dns-message'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 4);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode === 200 && !empty($response)) {
        echo $response;
        exit;
    }
}

// Fallback nếu Upstream không phản hồi
$respFlags = "\x81\x80";
$header = $txId . $respFlags . "\x00\x01\x00\x00\x00\x00\x00\x00";
echo $header . $qSection;

