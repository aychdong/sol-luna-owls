# 项目结构与重建 / Project structure and rebuild

| 目录 / Folder | 用途 / Purpose |
|---|---|
| `assets/approved/` | 已批准 R4 的完整精灵图与配置；发布不可重画 / Immutable approved R4 atlas inputs |
| `pets/` | 可直接安装的当前版 / Current installable release |
| `assets/baseline-r3/`, `assets/baselines/` | 比较及回退基线 / Comparison and rollback baselines |
| `assets/sources/`, `assets/prompts/` | 本次修复系列的生成原图与提示词 / Repair-series raw generations and prompts |
| `templates/`, `preview/`, `index.html` | 双语交互与动画预览 / Bilingual interactive and animation previews |
| `scripts/`, `reports/` | 构建、验证与发布清单 / Reproducible builds and validation |
| `archive/`, `workbench/` | 历史索引；大素材在 Release 附件 / History indexes; full materials in Release assets |
| `dist/` | 安装、交付、离线及回退下载包 / Generated download packages |
| `sol-luna-final/`, `releases/v1/` | 早期已提交目录，原样保留；不参与当前构建 / Previously committed legacy directories, retained unchanged and excluded from current builds |

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build_release.py
python3 scripts/build_preview.py
python3 scripts/validate_package.py
node scripts/check_preview.cjs
python3 scripts/package_downloads.py
```

构建直接复制 `assets/approved/`，不使用 imagegen，不依赖本地历史目录，不重新编码正式精灵图。动画 WebP 和网页从同一正式精灵图导出。`assets/provenance.json` 记录批准文件哈希。

Builds copy approved atlas bytes without image generation or atlas re-encoding. Preview assets are exported from those exact atlases. No private history directory or API key is needed. Approved hashes are recorded in `assets/provenance.json`.

后续更改请先放入独立 `workbench/` 子目录，记录基线、修改范围、提示词和对照。用户批准后再更新不可变输入、版本和校验记录。V9 与 V10 试作已归档；本次正式发布选择 V1 + R4，不从弃稿中拼装动作。

Future edits belong in separate workbench folders with baseline, scope, prompts and comparisons. Promote only after review. V9/V10 trials remain archived; the released artwork is V1 + R4.

完整历史 ZIP 解压到项目根目录可恢复 `archive/history/`、`archive/snapshots/` 和 `workbench/`。它保留早期图稿、生成图、备份 ZIP、审阅页和发布前根目录快照。源文件清单与校验和位于 `archive/source-archive-manifest.json`。

Extract the full history ZIP into the repository root to restore those three historical directories. It preserves early artwork, raw generations, backup ZIPs, review pages and the pre-release root snapshot. See `archive/source-archive-manifest.json` for the file inventory and hashes.
