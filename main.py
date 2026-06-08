import os
import sys

from langflow.load import run_flow_from_json

AUTH_ERROR_MARKERS = (
    "invalid api key",
    "invalid_api_key",
    "api_key client option must be set",
)

print("Đang khởi động quy trình tổng hợp tin tức AI...")

if not os.getenv("GROQ_API_KEY"):
    print("Thiếu GROQ_API_KEY, bỏ qua chạy luồng để tránh lỗi CI.")
    sys.exit(0)

# Gọi chạy luồng Langflow.
# Thuộc tính fallback_to_env_vars=True giúp bảo mật, tự động lấy API Key từ biến môi trường của GitHub.
try:
    result = run_flow_from_json(
        flow="AI_new.json",
        input_value="Kích hoạt quét tin tức",
        fallback_to_env_vars=True,
    )
except Exception as exc:
    error_text = str(exc).lower()
    if any(marker in error_text for marker in AUTH_ERROR_MARKERS):
        print("GROQ_API_KEY không hợp lệ, bỏ qua chạy luồng để tránh lỗi CI.")
        sys.exit(0)
    raise

print("Đã hoàn tất quy trình!")
