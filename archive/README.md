# 历史归档 / Archive

正式版仍是 **v1.1.0（V1 + R4）**。这里保留旧素材，避免与当前可安装的 `pets/` 混淆。整理采用移动并逐文件校验的方式，不删除历史，不改写 Git 历史。

| 路径 | 内容 | 保存位置 |
|---|---|---|
| `legacy/sol-luna-final/` | 最早的完整交付目录、原图、制作记录 | Git 仓库 |
| `legacy/releases/v1/` | 最初的安装 ZIP | Git 仓库 |
| `history/` | 早期设定图、试作与各轮审阅 | 本地；原发布历史 ZIP |
| `snapshots/` | 发布前根目录快照与 R1–R3 保留材料 | 本地；原发布历史 ZIP（具体内容见清单） |
| `workbench/` | 已结束的 V10、R1–R4 试作与朋友圈海报全部源文件 | 本地；旧试作在原历史 ZIP，海报另有补充归档 |
| `downloads/pre-organization/` | 旧 V9、V6 下载与历史解压目录 | 本地；旧源历史 ZIP 保留 |
| `organization-20260919/` | 整理前 Git 备份和校验基线 | 仅本地，不作为公开发布附件 |

- [目录迁移与逐文件哈希](organization-manifest.json)：记录每个原路径、新路径与原始 SHA-256。开发脚本随后只调整路径；图像和 ZIP 不变。
- [原发布历史素材清单](source-archive-manifest.json)：对应 **Sol-Luna-v1.1.0-source-history.zip**，在 [v1.1.0 Release](https://github.com/aychdong/sol-luna-owls/releases/tag/v1.1.0) 下载。
- [海报补充素材清单](sharing-guide-manifest.json)：对应 **Sol-Luna-sharing-guide-sources-2026-09-19.zip**，保留全部试排、验收版、源代码、字体与许可。
- `workbench/` 中原有网页入口保留为本地快捷路径，原审阅链接仍可打开。
- 重放历史脚本时，先在独立目录按当时的结构恢复；不要让旧脚本写入当前安装版。原历史 ZIP 的路径说明保持当时记录，可结合迁移清单查找新位置。

## English

The current release is still **v1.1.0 (V1 + R4)**. Legacy deliveries are in `legacy/`; large history, snapshots, completed workbench materials and obsolete downloads are retained locally. All moved files were hashed before and after the move. The relocation manifest maps old and new paths.

The existing **source-history ZIP** on GitHub remains unchanged and restores its original layout. A supplementary archive preserves the approved sharing poster and its source files. Original local review URLs remain accessible through shortcuts. Restore old build scripts into an isolated historical layout before running them. The local Git backup under `organization-20260919/` is deliberately excluded from public archives.
