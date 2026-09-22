---
name: rewrite-qc-feedback-vn
description: Viết lại ghi chú kỹ thuật thô của Nam thành phản hồi QC tiếng Việt ngắn gọn, lịch sự và có thể gửi ngay cho Dev, QA, BA/PO, quản lý, đối tác, shop hoặc khách hàng. Dùng khi cần soạn lại báo lỗi, kết quả kiểm tra log/API/payload/SQL, lỗi cấu hình, hiện trạng hệ thống, giới hạn truy vết, ảnh hưởng vận hành, yêu cầu hỗ trợ, đề xuất xử lý hoặc báo cáo escalation mà phải giữ nguyên dữ kiện kỹ thuật.
---

# Viết lại phản hồi QC

Chuyển ghi chú thô thành phản hồi rõ ràng theo mạch: hiện trạng, nguyên nhân, ảnh hưởng và hành động. Ưu tiên một bản hoàn chỉnh có thể sao chép và gửi ngay.

## Bảo toàn dữ kiện

- Giữ nguyên ID, tên hệ thống, tên trường, endpoint, giá trị, số lượng, tiền tệ, tỷ lệ, thời gian, trạng thái và quan hệ giữa các sự kiện.
- Không đổi thuật ngữ kỹ thuật nếu việc đổi từ có thể làm sai nghĩa. Đặt tên field, mã lỗi và giá trị code trong dấu backtick khi hữu ích.
- Phân biệt rõ dữ kiện quan sát được, nguyên nhân đã xác định, giả thuyết và thông tin chưa thể kết luận.
- Không tự bổ sung nguyên nhân, tác động, yêu cầu nghiệp vụ, mức độ nghiêm trọng hoặc người chịu trách nhiệm.
- Nếu ghi chú mâu thuẫn hoặc thiếu dữ kiện làm thay đổi kết luận, nêu ngắn gọn điểm chưa xác định; chỉ hỏi lại khi không thể tạo phản hồi an toàn.

## Quy trình

1. Trích xuất các ý bắt buộc: hiện trạng, bằng chứng, nguyên nhân hoặc giới hạn truy vết, ảnh hưởng, hành động và người nhận.
2. Loại bỏ từ lặp, câu đứt đoạn và lỗi chính tả nhưng không loại bỏ dữ kiện.
3. Sắp xếp nội dung theo thứ tự phù hợp:
   - **Hiện trạng:** Điều gì đang xảy ra hoặc kết quả kiểm tra.
   - **Nguyên nhân:** Nguyên nhân đã xác định; nếu chưa đủ log, nói rõ chưa xác định được từ dữ liệu hiện có.
   - **Ảnh hưởng:** Tác động thực tế đã được cung cấp.
   - **Hành động:** Việc cần làm, thứ tự thao tác, người cần kiểm tra hoặc đề xuất thay đổi.
4. Chọn nội dung và giọng điệu theo người nhận; xem phần **Theo người nhận**.
5. Kiểm tra lại từng con số, mã, field và phủ định trước khi trả lời.

## Theo người nhận

- **Dev/QA:** Nêu điều kiện xảy ra, actual, expected nếu có, bằng chứng kỹ thuật, phạm vi ảnh hưởng và nội dung cần kiểm tra. Giữ đủ ID, field, API, log hoặc bước tái hiện phục vụ điều tra.
- **BA/PO:** Nêu hành vi hiện tại, chênh lệch với nghiệp vụ hoặc requirement, ảnh hưởng vận hành và điểm cần xác nhận/quyết định. Không tự tạo expected result khi requirement chưa rõ.
- **Quản lý/BOD hoặc escalation:** Dùng SCQA ngắn gọn khi phù hợp: bối cảnh, vấn đề, ảnh hưởng/câu hỏi cần quyết định, đề xuất hành động. Đưa kết luận và mức độ ảnh hưởng lên trước.
- **Shop/khách hàng:** Dùng ngôn ngữ dễ hiểu, lịch sự và trung tính; hướng dẫn thao tác cụ thể. Chỉ nói lỗi cấu hình khi đã có bằng chứng và tránh đẩy trách nhiệm.
- **Đối tác tích hợp:** Chỉ rõ request/response, endpoint, field, timestamp, expected theo tài liệu hoặc thỏa thuận và nội dung cần đối tác xác minh.

Nếu người dùng không nêu người nhận, suy ra từ cách xưng hô, người được nhắc tên và mục đích của ghi chú. Khi vẫn chưa rõ, mặc định viết theo giọng team nội bộ, không thêm lời chào.

## Dạng phản hồi theo tình huống

- **Báo bug:** Hiện trạng/actual → expected đã có căn cứ → điều kiện hoặc bước tái hiện → ảnh hưởng → đề nghị kiểm tra.
- **Lỗi cấu hình:** Cấu hình hiện tại → điểm cấu hình chưa đúng → kết quả phát sinh → thao tác khắc phục theo thứ tự.
- **Chưa xác định nguồn:** Nêu những gì log chứng minh được → trường truy vết còn thiếu → kết luận giới hạn → dữ liệu hoặc đội cần hỗ trợ.
- **Đề xuất cải tiến:** Hạn chế hiện tại → tác động vận hành/tái sử dụng → thay đổi đề xuất → kết quả mong đợi.
- **Escalation:** Bối cảnh ngắn → vấn đề cần hỗ trợ → ảnh hưởng/phạm vi → bằng chứng → hành động hoặc quyết định cần từ người nhận.

## Quy tắc diễn đạt

- Mặc định viết một đoạn ngắn hoặc 2–4 đoạn/bullet khi có nhiều hành động.
- Dẫn bằng kết luận hoặc hiện trạng quan trọng nhất; không mở đầu dài dòng.
- Dùng câu chủ động và động từ hành động cụ thể như “tạm ngưng”, “cập nhật”, “kiểm tra”, “đối chiếu”, “kích hoạt lại”.
- Không thêm tiêu đề, bảng, lời chào hoặc câu kết nếu ghi chú ngắn và người dùng không yêu cầu.
- Không dùng từ “bug” như một kết luận khi chỉ có dấu hiệu nghi ngờ hoặc chưa đối chiếu requirement.
- Không biến lỗi cấu hình của shop thành lỗi hệ thống, hoặc ngược lại.
- Không dùng SCQA một cách máy móc cho phản hồi ngắn; chỉ dùng khi nội dung có nhiều bên liên quan, cần quyết định hoặc cần báo cáo tác động.
- Không công khai token, mật khẩu, thông tin xác thực hoặc dữ liệu cá nhân nhạy cảm có trong log; che phần nhạy cảm nhưng không làm mất dữ kiện cần điều tra.

## Mẫu đầu ra mặc định

`Hiện tại, [hiện trạng/bằng chứng]. Nguyên nhân [đã xác định/chưa thể xác định] là [nội dung]. Việc này [ảnh hưởng nếu có]. Nhờ [người/đội] [hành động cụ thể]; sau đó [bước tiếp theo nếu có].`

Điều chỉnh tự nhiên theo dữ liệu; không ép xuất hiện phần không có thông tin.

## Tự kiểm tra

Trước khi gửi, xác nhận rằng:

- Không mất hoặc thay đổi dữ kiện kỹ thuật quan trọng.
- Mức độ chắc chắn đúng với bằng chứng.
- Nguyên nhân, ảnh hưởng và hành động không bị trộn lẫn.
- Nội dung đủ lịch sự và ngắn gọn để gửi đúng đối tượng.
- Không có hành động được tự suy diễn ngoài ghi chú.
