# 测试元数据

- 用例 ID: `approved-report-performance-slo`
- 期望审核结果: `通过: Approved`
- 方向: 后端报表性能
- 格式: Markdown SLO 风格 Goal

> 使用 `$snap-goal-review` 测试时，只使用下面的“审核输入内容”部分。

# 审核输入内容

## Goal

将 staging 环境中 `monthly-report` 生成的 p95 延迟从当前基线降低到 30 秒以内，同时保留报表内容和 API 兼容性。

## 背景

大型客户在报表生成超过 30 秒时会放弃等待。性能提升不能以牺牲正确性为代价。

## 验收标准

1. 在 staging benchmark 数据集上，`monthly-report` p95 在连续 3 次 benchmark 中都低于 30 秒。
2. 报表内容在总计、行数和导出 CSV 字段上匹配当前 snapshot suite。
3. 现有报表 API 契约测试保持通过。
4. 变更文件证据显示只修改了 `backend/reports/`、报表测试和 benchmark 配置。

## 范围

包含：

- `backend/reports/`
- 报表测试
- benchmark 配置

不包含：

- 数据库 schema 修改
- 生产部署
- 前端报表 UI
- 计费逻辑

## 约束

- 不得修改数据库 schema。
- 不得删除报表字段。
- staging 计算成本增长不得超过 10%。
- 正确性优先于延迟，安全优先于成本。

## 事实来源

- 第一优先级：当前报表 API 契约测试。
- 第二优先级：snapshot suite。
- 第三优先级：benchmark 输出。
- 如果 benchmark 收益与 snapshot 正确性冲突，保留正确性并报告冲突。

## 完成证据

- 三次 p95 低于 30 秒的 benchmark 输出。
- 映射到内容保留验收标准的 snapshot 测试输出。
- API 契约测试输出。
- 变更文件列表。

## 停止与升级

- 所有验收标准通过且证据完成映射时完成。
- 连续 2 次尝试没有新证据、没有减少阻塞且没有合理替代路径时停止。
- schema 修改、生产修改、数据删除或成本增长超过 10% 前必须请求确认。

## 完成报告要求

报告：

- Unfinished
- Unverifiable
- Blocked
- Out of scope
- Residual risks
