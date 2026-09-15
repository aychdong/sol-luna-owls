# Sol & Luna · 日月猫头鹰

[中文](#中文介绍) · [English](#english)

![Sol and Luna character designs](sol-luna-final/预览/Sol-Luna-设计定稿.png)

## 中文介绍

**Sol & Luna** 是为 ChatGPT CodeX 桌面版 设计的一对日夜猫头鹰桌宠：白天的 **Sol** 与夜间的 **Luna**。Sol 在拉丁语中是表示太阳的阳性名词，Luna 表示月亮。

在希腊神话中，一只小猫头鹰（纵纹腹小鸮）代表着智慧女神雅典娜以及她在罗马神话中的化身弥涅耳瓦。由于这种联系，这种鸟通常被称为雅典娜的猫头鹰或密涅瓦的猫头鹰。在整个西方世界它成为知识、智慧、敏锐和博学的象征。

角色融合手绘羽毛质感与柔和的立体光影，保留大头、圆身、短腿、灵动眉羽、琥珀眼和金纹披风。日间版使用灰蓝羽毛与太阳主题配饰；夜间版使用深靛蓝羽毛与月亮主题配饰。

### 下载与安装

1. 下载 [Sol-Luna-安装包.zip](sol-luna-final/Sol-Luna-安装包.zip) 并解压，或通过 **Code → Download ZIP** 下载整个项目。
2. 将 `sol`、`luna` 两个文件夹复制到 `~/.codex/pets/`。macOS Finder 可按 **⌘ ⇧ G** 输入这个路径。
3. 在支持本地宠物的 Codex / ChatGPT 桌面应用中，打开 **设置 → 宠物 → 刷新**，选择 **Sol · 晨光** 或 **Luna · 月夜**，然后显示／唤醒宠物。

```text
~/.codex/pets/
├── sol/
│   ├── pet.json
│   └── spritesheet.webp
└── luna/
    ├── pet.json
    └── spritesheet.webp
```

无需运行代码。请勿多套一层目录；已有同名宠物时先备份。日夜版需手动切换。

### 双语动画展示

下载项目后，双击根目录的 **index.html**，或打开 [离线动画预览](sol-luna-final/预览/动画预览.html)。点击右上角 **中文 / English** 切换完整界面语言，选择会在浏览器允许时记住。

支持 9 组动作、16 个观察方向帧、大小和速度调整、暂停、浅深色背景及透明边缘检查。预览完全离线，无追踪、无外部字体或网络依赖。GitHub 的文件页面显示源码；请下载 HTML 后用浏览器打开。

### 项目内容

| 路径 | 内容 |
| --- | --- |
| `index.html` | 中英双语展示页 |
| `sol-luna-final/可直接安装/` | 两个可直接复制的宠物包 |
| `sol-luna-final/预览/` | 设计稿、实际角色帧、动画与离线展示 |
| `sol-luna-final/制作记录/` | 原始素材、提示词、制作脚本及检查记录 |
| `scripts/build_preview.py` | 重建双语展示和文件校验清单 |

### 规格与验证

桌面 v2 精灵图采用透明无损 WebP：**1536 × 2288**，**8 × 11** 格，每格 **192 × 208**。两套文件已检查 88 格有效内容、透明背景、格内边界和无损回读，并通过本机应用 **26.901.51231** 的图像格式校验函数。原生应用中的实际选择和播放未做自动验证；未来版本的兼容性仍需以应用为准。网页版上传规格不同。

素材由 imagegen 生成，随后经授权使用本地 Python / Pillow / NumPy 抠图、对齐和打包。原始素材保留不变。

## English

**Sol & Luna** are a pair of day-and-night owl companions created for ChatGPT CodeX desktop apps. **Sol** is the masculine Latin noun for the sun; **Luna** means the moon.

In Greek mythology, a little owl (Athene noctua) traditionally represents or accompanies Athena, the virgin goddess of wisdom, or Minerva, her syncretic incarnation in Roman mythology. Because of such association, the bird—often referred to as the "owl of Athena" or the "owl of Minerva"—has been used as a symbol of knowledge, wisdom, perspicacity and erudition throughout the Western world

Their design combines hand-painted feathers with soft dimensional lighting: large expressive heads, rounded bodies, short legs, lively brow feathers, amber eyes, and gold-patterned capes. Sol wears slate-blue plumage and solar accents; Luna wears deep indigo with lunar accents.

### Download and install

1. Download and extract [Sol-Luna-安装包.zip](sol-luna-final/Sol-Luna-安装包.zip), or download the whole repository using **Code → Download ZIP**.
2. Copy the `sol` and `luna` folders into `~/.codex/pets/`. In macOS Finder, press **⌘ ⇧ G** to open that path.
3. In a Codex / ChatGPT desktop app that supports local pets, open **Settings → Pets → Refresh**, select **Sol · 晨光** or **Luna · 月夜**, and show or wake the pet.

Each pet folder must directly contain `pet.json` and `spritesheet.webp`, as shown in the folder tree above. No scripts are needed for installation. Back up existing folders with the same names. Day/night variants are selected manually.

### Bilingual animation showcase

After downloading, open **index.html** or the [standalone offline preview](sol-luna-final/预览/动画预览.html) in a browser. The **中文 / English** button translates all interface text and remembers your preference when browser storage is available.

The preview includes nine action sequences, sixteen directional frames, size and speed controls, pause/play, light/dark backgrounds, and transparency inspection. It runs offline without analytics, external fonts, or network dependencies. GitHub displays HTML as source; download it to view it in your browser.

### Repository contents

| Path | Contents |
| --- | --- |
| `index.html` | Bilingual showcase |
| `sol-luna-final/可直接安装/` | Ready-to-copy pet packages |
| `sol-luna-final/预览/` | Concept art, actual frames, animations, and offline preview |
| `sol-luna-final/制作记录/` | Generated source assets, prompts, scripts, and validation reports |
| `scripts/build_preview.py` | Rebuilds the showcase and checksums |

### Format and validation

Desktop v2 uses transparent, lossless WebP sheets: **1536 × 2288 pixels**, an **8 × 11 grid**, and **192 × 208 cells**. Both packages were checked for populated frames, alpha transparency, cell bounds, and pixel-exact lossless round trips. They also passed the image-validation function from installed app version **26.901.51231**. Native pet selection and playback were not automatically exercised; future app versions may differ. Web pet uploads use a different size.

Artwork was generated with imagegen and processed locally using authorized Python / Pillow / NumPy extraction, alignment, and packaging. Generated originals are preserved.

### Rebuild / 重新构建

Requires Python 3, Pillow, and NumPy / 需要 Python 3、Pillow 和 NumPy：

```sh
python3 -m pip install pillow numpy
python3 sol-luna-final/制作记录/build_pets.py
python3 scripts/build_preview.py
```

The second command rebuilds the preview, installation ZIP, and checksums. / 第二条命令会重建展示页、安装 ZIP 和校验清单。

### References / 参考

- [Official pet documentation / 官方宠物说明](https://learn.chatgpt.com/zh-Hans/docs/pets)
- [Lewis and Short: sōl](https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:lat.ls.perseus-eng2-n44583/)

This is a personal art project, not an official OpenAI product. No open-source license has been granted in this repository. / 这是个人艺术项目，并非 OpenAI 官方产品；本仓库尚未授予开源许可。
