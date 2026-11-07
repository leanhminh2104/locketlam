/**
 * ==============================================================================
 * GÓI LOCKET FREE DO LAMDEV x DALYMMO.COM PHÁT HÀNH
 * Cloudflare Worker DNS-over-HTTPS (DoH) Server - Chuẩn RFC 8484
 * 
 * 🌐 Website: https://dalymmo.com
 * 🛠 Phát hành bởi: LAMDev x DaLyMMO.com
 * ⚡ Tốc độ cao - Không giới hạn truy vấn - Không lo quảng cáo / chặn bot
 * ==============================================================================
 */

const BLOCKED_DOMAINS = [
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

export default {
  async fetch(request, env, ctx) {
    // Xử lý CORS Preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Accept'
        }
      });
    }

    let dnsQueryBuffer = null;

    if (request.method === 'GET') {
      const url = new URL(request.url);
      const dnsParam = url.searchParams.get('dns');
      if (dnsParam) {
        // Giải mã Base64URL
        let base64 = dnsParam.replace(/-/g, '+').replace(/_/g, '/');
        while (base64.length % 4) base64 += '=';
        const binaryStr = atob(base64);
        const bytes = new Uint8Array(binaryStr.length);
        for (let i = 0; i < binaryStr.length; i++) {
          bytes[i] = binaryStr.charCodeAt(i);
        }
        dnsQueryBuffer = bytes.buffer;
      }
    } else if (request.method === 'POST') {
      dnsQueryBuffer = await request.arrayBuffer();
    }

    // Nếu không có truy vấn DNS -> Trả về Dashboard HTML
    if (!dnsQueryBuffer || dnsQueryBuffer.byteLength < 12) {
      return new Response(getLandingHTML(), {
        status: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8' }
      });
    }

    const queryBytes = new Uint8Array(dnsQueryBuffer);
    const txId = queryBytes.slice(0, 2);

    // Phân tích tên miền truy vấn từ Question Section
    let offset = 12;
    const domainParts = [];
    while (offset < queryBytes.length) {
      const labelLen = queryBytes[offset];
      if (labelLen === 0) {
        offset++;
        break;
      }
      offset++;
      if (offset + labelLen > queryBytes.length) break;
      const part = new TextDecoder().decode(queryBytes.subarray(offset, offset + labelLen));
      domainParts.push(part);
      offset += labelLen;
    }

    const queryDomain = domainParts.join('.').toLowerCase();
    let qType = 0;
    let qSection = null;

    if (offset + 4 <= queryBytes.length) {
      qType = (queryBytes[offset] << 8) | queryBytes[offset + 1];
      qSection = queryBytes.subarray(12, offset + 4);
    }

    // Kiểm tra xem tên miền có trong Blocklist không
    const isBlocked = BLOCKED_DOMAINS.some(
      b => queryDomain === b || queryDomain.endsWith('.' + b)
    );

    if (isBlocked && qSection) {
      // Trả lời Sinkhole 0.0.0.0 hoặc ::
      const respFlags = new Uint8Array([0x81, 0x80]); // QR=1, RD=1, RA=1, RCODE=0
      let responseBytes;

      if (qType === 1) { // Type A: 0.0.0.0
        const header = new Uint8Array([...txId, ...respFlags, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]);
        const answer = new Uint8Array([0xc0, 0x0c, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x01, 0x2c, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00]);
        responseBytes = new Uint8Array(header.length + qSection.length + answer.length);
        responseBytes.set(header, 0);
        responseBytes.set(qSection, header.length);
        responseBytes.set(answer, header.length + qSection.length);
      } else if (qType === 28) { // Type AAAA: ::
        const header = new Uint8Array([...txId, ...respFlags, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]);
        const answer = new Uint8Array([0xc0, 0x0c, 0x00, 0x1c, 0x00, 0x01, 0x00, 0x00, 0x01, 0x2c, 0x00, 0x10, ...new Array(16).fill(0)]);
        responseBytes = new Uint8Array(header.length + qSection.length + answer.length);
        responseBytes.set(header, 0);
        responseBytes.set(qSection, header.length);
        responseBytes.set(answer, header.length + qSection.length);
      } else { // NODATA
        const header = new Uint8Array([...txId, ...respFlags, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]);
        responseBytes = new Uint8Array(header.length + qSection.length);
        responseBytes.set(header, 0);
        responseBytes.set(qSection, header.length);
      }

      return new Response(responseBytes, {
        status: 200,
        headers: {
          'Content-Type': 'application/dns-message',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=300'
        }
      });
    }

    // Chuyển tiếp tới Cloudflare 1.1.1.1 cho các tên miền bình thường
    return fetch('https://1.1.1.1/dns-query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/dns-message',
        'Accept': 'application/dns-message'
      },
      body: dnsQueryBuffer
    });
  }
};

function getLandingHTML() {
  return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gói Locket Free - LAMDev x DaLyMMO.com</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background: #0b0f19; color: #f3f4f6; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
    .container { background: #111827; border: 1px solid #1f2937; border-radius: 20px; padding: 36px 30px; max-width: 560px; width: 100%; box-shadow: 0 20px 50px rgba(0,0,0,0.6); position: relative; }
    .badge { display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 9999px; font-size: 13px; font-weight: 600; margin-bottom: 20px; }
    h1 { font-size: 24px; font-weight: 800; color: #f59e0b; margin-bottom: 8px; }
    .author { font-size: 14px; color: #9ca3af; margin-bottom: 16px; }
    .author span { color: #38bdf8; font-weight: 700; }
    p { font-size: 14px; line-height: 1.6; color: #9ca3af; margin-bottom: 24px; }
    .card { background: #1a2234; border: 1px solid #28334e; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px; font-size: 13px; display: flex; justify-content: space-between; }
    .btn { display: block; text-align: center; padding: 14px; background: #f59e0b; color: #000; border-radius: 12px; font-weight: 700; text-decoration: none; margin-bottom: 20px; }
    .footer { text-align: center; font-size: 12px; color: #6b7280; }
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">● Cloudflare Edge DoH Online</div>
    <h1>💛 Gói Locket Free</h1>
    <div class="author">Phát hành bởi: <span>LAMDev x DaLyMMO.com</span></div>
    <p>Máy chủ DNS-over-HTTPS Cloudflare Worker tốc độ cao, 100% miễn phí không giới hạn truy vấn, bảo vệ Locket Gold VIP và chống thu hồi chứng chỉ Apple.</p>
    <div class="card">
      <span style="color:#94a3b8;">Trạng thái:</span>
      <span style="color:#4ade80; font-weight: 700;">Hoạt động 100%</span>
    </div>
    <a href="https://dalymmo.com" target="_blank" class="btn">🌐 Mở Website DaLyMMO.com</a>
    <div class="footer">&copy; Gói Locket Free do LAMDev x DaLyMMO.com phát hành</div>
  </div>
</body>
</html>`;
}

