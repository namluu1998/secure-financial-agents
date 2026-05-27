# Mô tả Bug

## Tiêu đề

`[Khu vực chức năng] Mô tả ngắn gọn lỗi và ảnh hưởng`

## Môi trường

| Trường | Giá trị |
|---|---|
| Hệ thống | [Dev / Staging / Production; OS/app version nếu có] |
| Trang | [URL hoặc màn hình/tính năng] |
| Trình duyệt | [Tên + phiên bản; thiết bị nếu liên quan] |
| Build/Version | [Mã build, release, commit nếu có] |
| Tài khoản/Quyền | [Vai trò đang dùng, không ghi credential] |

## Mức độ

`[Critical / High / Medium / Low]` - [Lý do dựa trên ảnh hưởng và phạm vi]

## Mô tả vấn đề

[Mô tả triệu chứng, tần suất, người dùng/dữ liệu bị ảnh hưởng. Nếu kỳ vọng chưa được xác định bởi requirement, ghi rõ đây là giả định cần xác minh.]

## Các bước tái hiện

### Điều kiện tiên quyết

- [Dữ liệu khởi tạo, quyền truy cập, cấu hình, hoặc điều kiện cần có]

### Bước thực hiện

1. [Bước 1]
2. [Bước 2]
3. [Bước 3]

## Kết quả thực tế vs Mong đợi

| Nội dung | Chi tiết |
|---|---|
| Kết quả thực tế | [Hành vi quan sát được, lỗi/thông báo nếu có] |
| Kết quả mong đợi | [Hành vi đúng theo requirement/acceptance criteria/design/API contract] |
| Nguồn mong đợi | [Link tài liệu, ticket, AC, hoặc hành vi đã xác minh trước đó] |

## Nguyên nhân nghi ngờ

[Nếu có bằng chứng kỹ thuật, nêu nguyên nhân khả dĩ và vì sao. Nếu chưa có, ghi `Chưa xác định - cần điều tra`, không kết luận vô căn cứ.]

## Bằng chứng

- Ảnh chụp/video: [đường dẫn hoặc file đính kèm]
- Log/console/network: [đoạn trích đã che dữ liệu nhạy cảm]
- Request/response: [chỉ ghi sau khi đã ẩn token và dữ liệu cá nhân]
- Test bị fail: [test case ID hoặc link automation run]

## Ảnh hưởng và phạm vi

- Người dùng/chức năng bị ảnh hưởng: [nội dung]
- Khả năng tái hiện: [Always / Intermittent / Once / Chưa xác nhận]
- Workaround: [Có/Không; mô tả nếu có]
- Rủi ro bảo mật/quyền riêng tư/dữ liệu: [Có/Không/Chưa đánh giá]

## Ghi chú triển khai

- Ưu tiên đề xuất: [P0/P1/P2/P3 và lý do]
- Test hồi quy cần chạy: [danh sách]
- Thông tin còn thiếu: [danh sách]

> Không đưa mật khẩu, API key, session token, dữ liệu cá nhân, số tài khoản hoặc tài liệu nhạy cảm chưa che vào task.
