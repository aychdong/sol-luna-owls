# 项目结构 / Project map

当前正式版：**v1.1.0 / V1 + R4**。本次目录整理不改变宠物素材、安装包或版本号。

| 根目录路径 | 用途 |
|---|---|
| `README.md`, `docs/INSTALL.md` | 面向使用者的双语介绍与安装说明 |
| `pets/` | 当前可直接安装的两只宠物 |
| `preview/`, `index.html` | 当前素材的动画与双语在线展示 |
| `media/` | 原始设定海报与用户验收的一页图解 |
| `development/` | 源素材、提示词、构建、模板、验证与技术记录 |
| `archive/` | 历史索引；旧交付物归档；完整本地历史 |
| `workbench/` | 后续试作入口；旧网址以本地快捷路径保留 |
| `dist/` | 已发布安装包与下载文件，本地保留，GitHub Release 分发 |

详见 [制作与维护](../README.md) 及 [归档索引](../../archive/README.md)。

## 验收边界

批准的 `pet.json` 和精灵图在 `development/assets/approved/`。构建直接复制，批准哈希在 `development/assets/provenance.json`。两只各 1536 × 2288、8 × 11 格、单格 192 × 208，v2 无损透明 WebP。

当前所有前九行动作与 V1 相同；视线修复使用批准的 R4。`validate_package.py` 检查批准文件字节、V1 动作像素、R3 差异范围、时间轴和 ZIP 文件层级。网页测试检查方向、动作、语言、播放速度和资源链接；它不替代原生应用触发实测。

## English

`pets/`, `preview/`, `media/` and the root overview are user-facing. `development/` contains reproducible inputs and tooling. `archive/` preserves previous releases and review materials; `workbench/` is reserved for new trials, with local shortcuts retaining earlier review URLs. `dist/` contains release downloads, distributed through GitHub Releases.

The approved v1.1.0 artwork is unchanged by this organization. Build and validation instructions are in [Development & maintenance](../README.md). Native event behavior must be tested separately from web controls.
