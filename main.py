import os
import sys

from langflow.load import run_flow_from_json

AUTH_ERROR_MARKERS = (
    "invalid api key",
    "invalid_api_key",
    "api_key client option must be set",
)
AUTH_EXCEPTION_NAMES = {"AuthenticationError", "GroqError"}


def is_groq_auth_error(exc: Exception) -> bool:
    current = exc
    while current:
        if current.__class__.__name__ in AUTH_EXCEPTION_NAMES:
            return True

        if any(marker in str(current).lower() for marker in AUTH_ERROR_MARKERS):
            return True

        current = current.__cause__ or current.__context__

    return False

if not os.getenv("GROQ_API_KEY"):
    print("Thiếu GROQ_API_KEY, bỏ qua chạy luồng để tránh lỗi CI.")
    sys.exit(0)

print("Đang khởi động quy trình tổng hợp tin tức AI...")

# Gọi chạy luồng Langflow.
# Thuộc tính fallback_to_env_vars=True giúp bảo mật, tự động lấy API Key từ biến môi trường của GitHub.
try:
    result = run_flow_from_json(
        flow="AI_new.json",
        input_value="Kích hoạt quét tin tức",
        fallback_to_env_vars=True,
    )
except Exception as exc:
    if is_groq_auth_error(exc):
        print(f"GROQ_API_KEY không hợp lệ, bỏ qua chạy luồng để tránh lỗi CI. Chi tiết: {exc}")
        sys.exit(0)
    raise

print("Đã hoàn tất quy trình!")
