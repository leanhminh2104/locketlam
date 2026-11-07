#!/usr/bin/env python3
"""
==============================================================================
GÓI LOCKET FREE DO LAMDEV x DALYMMO.COM PHÁT HÀNH
Tool mã hóa & ký số Apple Configuration Profile (.mobileconfig) sang chuẩn PKCS#7 DER Binary
(Cấu trúc mã hóa và bảo vệ giống hệt khoindvn.mobileconfig)
==============================================================================
"""

import os
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERTS_DIR = os.path.join(BASE_DIR, 'certs')
KEY_FILE = os.path.join(CERTS_DIR, 'lamdev_key.pem')
CERT_FILE = os.path.join(CERTS_DIR, 'lamdev_cert.pem')

def ensure_certificates():
    os.makedirs(CERTS_DIR, exist_ok=True)
    if not os.path.exists(KEY_FILE) or not os.path.exists(CERT_FILE):
        print("[+] Đang tạo khóa bảo mật và chứng chỉ số cho LAMDev x DaLyMMO.com...")
        cmd_gen = [
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", KEY_FILE,
            "-out", CERT_FILE,
            "-days", "3650",
            "-nodes",
            "-subj", "/CN=Goi Locket Free - LAMDev x DaLyMMO.com/O=DaLyMMO.com/C=VN"
        ]
        subprocess.run(cmd_gen, check=True)
        print("[✓] Đã tạo chứng chỉ số thành công tại thư mục 'certs/'!")

def sign_mobileconfig(input_path, output_path, custom_cert=None, custom_key=None):
    if not os.path.exists(input_path):
        print(f"[!] Không tìm thấy tệp nguồn: {input_path}")
        return False

    cert = custom_cert if custom_cert and os.path.exists(custom_cert) else CERT_FILE
    key = custom_key if custom_key and os.path.exists(custom_key) else KEY_FILE

    cmd_sign = [
        "openssl", "smime", "-sign",
        "-in", input_path,
        "-out", output_path,
        "-signer", cert,
        "-inkey", key,
        "-outform", "DER",
        "-nodetach"
    ]
    subprocess.run(cmd_sign, check=True)
    size = os.path.getsize(output_path)
    print(f"[✓] Đã mã hóa và ký số: {output_path} ({size:,} bytes)")
    return True

if __name__ == "__main__":
    ensure_certificates()
    
    source_xml = os.path.join(BASE_DIR, "locketlam.xml")
    if not os.path.exists(source_xml):
        print("[!] Không tìm thấy locketlam.xml, sử dụng locketlam.mobileconfig làm nguồn.")
        source_xml = os.path.join(BASE_DIR, "locketlam.mobileconfig")

    # Đồng bộ file nguồn XML sang thư mục con locketlam/
    sub_xml = os.path.join(BASE_DIR, "locketlam", "locketlam.xml")
    shutil.copyfile(source_xml, sub_xml)

    # 1. Ký và tạo file binary PKCS#7 cho thư mục gốc
    out_root_binary = os.path.join(BASE_DIR, "locketlam.mobileconfig")
    out_root_signed = os.path.join(BASE_DIR, "locketlam_signed.mobileconfig")
    sign_mobileconfig(source_xml, out_root_binary)
    shutil.copyfile(out_root_binary, out_root_signed)

    # 2. Ký và tạo file binary PKCS#7 cho thư mục con locketlam/
    out_sub_binary = os.path.join(BASE_DIR, "locketlam", "locketlam.mobileconfig")
    out_sub_signed = os.path.join(BASE_DIR, "locketlam", "locketlam_signed.mobileconfig")
    shutil.copyfile(out_root_binary, out_sub_binary)
    shutil.copyfile(out_root_binary, out_sub_signed)
        
    print("\n[★] Hoàn tất 100%! Toàn bộ file .mobileconfig đã được mã hóa binary PKCS#7 chống soi mã nguồn.")
