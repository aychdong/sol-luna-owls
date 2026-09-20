# 制作与维护 / Development & maintenance

此目录存放制作、验证与发布资料。给使用者的安装说明在根目录 README 和 `docs/INSTALL.md`。

The user-facing overview and installation guide remain at the repository root. Build internals, review records and source assets live here.

| 路径 / Path | 内容 / Contents |
|---|---|
| `assets/approved/` | 当前批准的精灵图与配置，构建直接复制 / Byte-exact approved inputs |
| `assets/baselines/`, `assets/baseline-r3/` | 原版及 R3 比较与回退基线 / Original and R3 baselines |
| `assets/sources/`, `assets/prompts/` | 生成原图、提示词 / Generation sources and prompts |
| `scripts/`, `requirements.txt` | 构建与校验 / Build and validation |
| `templates/preview.html` | 用户预览页模板 / Public preview template |
| `review.html` | 旧 R3/R4 技术对照页 / Retained technical comparison |
| `reports/` | 包、动画和页面的验证记录 / Validation reports |
| `docs/` | 技术历史、审阅及发布记录 / Technical history and review notes |

## 构建 / Build

从仓库根目录执行。建议指定独立输出目录，避免覆盖已发布的 ZIP：

Run from the repository root. Use a separate output directory to avoid replacing published archives:

```sh
python3 -m pip install -r development/requirements.txt
export SOL_LUNA_DIST=/tmp/sol-luna-build
python3 development/scripts/build_release.py
python3 development/scripts/build_preview.py
python3 development/scripts/validate_package.py
node development/scripts/check_preview.cjs
python3 development/scripts/package_downloads.py
```

`build_release.py` 会从批准输入重建 `pets/` 与 `preview/`；`build_preview.py` 会更新根目录 `index.html`。它们不重新生成角色，不需要 API 密钥。包输出默认为本地 `dist/`。发布新版本前更新版本号、审阅记录和校验清单，不覆盖旧版本的 Release 附件。

The artwork is copied from approved inputs, never regenerated. The build updates `pets/`, `preview/` and `index.html`; package outputs default to `dist/`. Keep published release assets immutable. No API key or local archive is required.

海报完整源文件仅在本地保存，不能作为 Release 附件公开上传。历史归档脚本默认排除此目录；Git 备份也不进入公开归档。已验收的最终分享图可在 `media/` 中公开展示。

Complete sharing-poster sources are local-only and excluded from shareable history archives. Local Git backups are also excluded. Only approved final poster images are published in `media/`.

## 历史与后续修改 / History & future edits

- 当前正式素材为 **V1 + R4 / v1.1.0**，不混用后续弃稿。
- 新试作放 `workbench/<topic>/`，记录基线和修改范围；用户批准后才提升为正式素材。
- [归档索引](../archive/README.md)记录历史、回退包和本地路径。旧版本文件均保留；不要对 Git 历史做强制改写。
- [项目与验收说明](docs/PROJECT.md)、[审阅记录](docs/REVIEW.md)、[历史变更](docs/CHANGELOG.md)。

New trials require explicit review before promotion. Native trigger checks are distinct from web preview tests; do not claim an app interaction was tested based only on a browser preview.
