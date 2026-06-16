# Career Agent — managed-agent template

## Overview

Hệ thống AI career operating system hoạt động như một headhunter cá nhân. Phân tích Career DNA của ứng viên, tìm và xếp hạng việc làm phù hợp, tối ưu hóa CV, chuẩn bị phỏng vấn, và hỗ trợ thương lượng lương. Nguồn giống plugin [`career-agent`](../../plugins/agent-plugins/career-agent) — thư mục này là Managed Agent cookbook cho `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export JOBS_MCP_URL=...
export SALARY_MCP_URL=...
../../scripts/deploy-managed-agent.sh career-agent
```

## Steering events

Xem [`steering-examples.json`](./steering-examples.json).

## Security & handoffs

Tài liệu ứng viên là untrusted. Phân tách 5 tầng worker:

| Worker | Đọc tài liệu untrusted? | Tools | Connectors |
|---|---|---|---|
| **`career-dna`** | **Có** | `Read`, `Grep` only | Không có |
| `job-matcher` | Không | `Read`, `Grep` | jobs (read-only) |
| `interview-agent` | Không | `Read`, `Grep` | Không có |
| `salary-agent` | Không | `Read` | salary (read-only) |
| **`resume-tailor`** (Write-holder) | Không | `Read`, `Write`, `Edit` | Không có |

Orchestrator validate output của `career-dna` theo `output_schema` trước khi truyền cho bất kỳ worker nào. `resume-tailor` tạo file vào `./out/resume-<candidate>-<job>-v<n>.md` và `./out/cover-<candidate>-<job>-v<n>.md`.

**Auto-apply không được triển khai** trong cookbook này. Mọi việc nộp đơn đều yêu cầu sự đồng ý rõ ràng của người dùng cho từng công việc, được lưu trước khi `apply` được gọi.

**Lưu ý:** Career Score và Match Score là ước tính của model — luôn hiển thị khoảng tin cậy và giải thích để ứng viên tự quyết định.
