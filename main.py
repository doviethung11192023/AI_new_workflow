from langflow.load import run_flow_from_json

print("Đang khởi động quy trình tổng hợp tin tức AI...")

# Gọi chạy luồng Langflow.
# Thuộc tính fallback_to_env_vars=True giúp bảo mật, tự động lấy API Key từ biến môi trường của GitHub.
result = run_flow_from_json(
    flow="AI_new.json",
    fallback_to_env_vars=True
)

print("Đã hoàn tất quy trình!")