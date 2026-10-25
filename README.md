# Price Radar · 看板

统一管理价格大盘、参考报价、策略实验和 Python 量化计算。

- `apps/dashboard/` — 正式大盘（待从 Vercel 完整导入）
- `apps/reference/` — 参考价格看板（待导入）
- `apps/strategy/` — 策略实验（待从 Vercel 完整导入）
- `packages/quant/` — NumPy/Pandas 清洗与统计
- `.github/workflows/quant.yml` — 定时量化测试与离线分析

**状态：迁移中。** 原有 Vercel 生产部署不受本仓库影响。未核实参考价不得混入正式价格曲线。