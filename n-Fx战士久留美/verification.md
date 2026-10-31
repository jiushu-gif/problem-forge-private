# 验题记录

- 底本：洛谷 B2091《向量点积计算》（1.00s / 128.00 MB）。本题保留原做法与数据范围，加入《FX 战士久留美》背景：一个数组是每笔仓位的本金，另一个数组是杠杆，逐项相乘再求和得到账户最终金额。
- `forge.py check`：私有仓库 6 个题目目录（含 `vector-dot-product`）通过结构检查。
- 数据与答案：`data/samples` 1 对、`data/tests` 12 对，`.in` / `.out` 一一对应；全部输入通过结构校验（行数与 `n` 匹配、`1 ≤ n ≤ 1000`、`|a_i|,|b_i| ≤ 1000`），答案文件与独立计算一致。定向用例覆盖 `n=1`、全零、负数、`n=999`、`n=1000`、以及每维取 ±1000 使答案达到 ±10^9 的极值。
- 双解交叉验证：`solution.cpp`（C++20，`long long` 累加）与独立实现 `solution2.py` 在全部 13 个用例、500 组随机数据上输出一致。
- 错误解验题：`wrong_off_by_one.cpp`（少算最后一笔仓位）被 11 个用例拒绝；`wrong_reuse_a.cpp`（只读本金、把本金当杠杆，误算自身平方和）被 7 个用例拒绝。
- 数据生成器：`generator.py` 六种类型（min / max / random / small / zeros / edge）各 4 个种子，生成的输入全部合法且与双解一致。
- 题面：`statement.pdf` 为单页，页眉「2026 HHACM 招新赛」、`Problem N`、四项运行信息齐全；`render_preview.py` 校验页眉、题号、四项运行信息、各小节、正文关键词（久留美 / 本金 / 杠杆）与样例文本均可见。已目视检查：中文与上下标正常、无英文单词跨行截断、无行首标点、样例行首运算符按数学续行处理、表格边框与对齐正常、PDF 内不含题解。
- 排版脚本 `build_statement.py` 使用自带 CJK 断行（禁则 + 拉丁词不拆行 + 行尾空格修剪），并支持 `_{i}` 下标与 `^{4}` 上标；修改正文后需重新渲染并目视检查。
- Hydro 导出包：标题已改为「久留美的 FX 账户」（`problem.json`、题面 H1、`problem.yaml`、包名同步）；pid 为 `ZXS2026N`，包名为 `N-久留美的 FX 账户.zip`（按「N-题名」命名，未改成 `N-ZXS2026N`）；`problem.yaml` 的 `pid: ZXS2026N`、`title: 久留美的 FX 账户`；`problem_zh.md` 为 `@[pdf](file://statement.pdf)`；`additional_file/statement.pdf` 与内部原件字节一致；`testdata` 含 `sample01` 与 `case01–12`，`.in` / `.ans` 共 13 对一一对应，`config.yaml` 为 `type: default`、`time: 1s`、`memory: 128m`（读取自 `problem.json`）；压缩包 30 个条目与导出目录一致。
- 尚待在目标 Hydro 实例验证导入与中文包名、PDF 嵌入是否正常；当前不能声称压缩包已在该实例直接导入成功。
