# 安装与使用 / Installation & use

[返回首页 / Back to the overview](../README.md) · [下载安装包 / Download](https://github.com/aychdong/sol-luna-owls/releases/download/v1.1.0/Sol-Luna-v1.1.0-install.zip)

## macOS 安装

1. 下载 `Sol-Luna-v1.1.0-install.zip`，双击解压。
2. Finder 按 **⌘ ⇧ G**，输入 `~/.codex/pets/`。如果不存在，先进入 `~/.codex/`，新建名为 `pets` 的文件夹。
3. 将解压出的 **sol** 和 **luna** 两个文件夹复制进去。已有同名文件夹时，先移到其他位置备份。
4. 打开 Codex **设置 → 宠物**，刷新，选择 **Sol · 晨光** 或 **Luna · 月夜**，点击唤醒／显示宠物。

正确的层级如下；不要把外面的 ZIP 名称文件夹一起套进去：

```text
~/.codex/pets/
├── sol/
│   ├── pet.json
│   └── spritesheet.webp
└── luna/
    ├── pet.json
    └── spritesheet.webp
```

## 日常互动

安装后，所选猫头鹰浮在桌面上。悬停会轻跃，左右拖动会跑步，应用工作时会敲电脑。其他动作由应用任务状态触发。Sol 和 Luna 需要手动切换，不会按时间自动切换。

[在线预览](https://aychdong.github.io/sol-luna-owls/)可以查看所有动作及视线方向，但不会操控已安装的宠物。应用版本、任务状态和减少动态效果设置可能影响实际表现。

## 更新、回退与卸载

- **更新：** 备份旧文件夹，复制新文件夹，刷新后重新选择。若仍显示旧图，完整退出应用再打开。
- **回退：** 用自己的备份，或发布页的 `Sol-Luna-V1-original-rollback.zip` / `Sol-Luna-R3-rollback.zip` 替换同名文件夹。它们是历史版本，视线表现可能与当前版不同。
- **隐藏：** 使用宠物菜单中的隐藏选项。
- **卸载：** 先选择其他宠物，再将 `sol` 和 `luna` 移出 `~/.codex/pets/`，保留其他宠物文件夹。

没有“宠物”入口时，请检查桌面应用更新。这份说明针对 macOS 自定义宠物；网页版的上传流程不同，Windows 安装过程暂未验证。

## English

1. Download and extract `Sol-Luna-v1.1.0-install.zip`.
2. In Finder, press **⌘ ⇧ G** and open `~/.codex/pets/`. If missing, open `~/.codex/` and create a `pets` folder.
3. Copy **sol** and **luna** into it, backing up any existing folders elsewhere first. Each pet folder must directly contain `pet.json` and `spritesheet.webp`, as shown above.
4. Open **Settings → Pets**, refresh, select **Sol** or **Luna**, then **Wake / Show pet**.

The selected owl floats on your desktop. Hover for a hop, drag for running, and watch it type while the app works. Other animations depend on the application's state and settings. Switch characters manually; this project does not add automatic day/night switching.

**Update:** back up, replace the folders, refresh and select again. Fully quit and reopen the app if old artwork remains. **Roll back:** restore your backup or a historical rollback ZIP from the release page. **Remove:** select another pet, then move only the `sol` and `luna` folders out. To simply hide it, use the pet menu.

If Pets is absent from Settings, check for app updates. These instructions cover macOS desktop custom pets; web uploads use a different workflow, and Windows installation has not been verified here.

---

应用的宠物入口与功能说明 / Application feature reference: [Pets 官方说明 / Official Pets guide](https://learn.chatgpt.com/zh-Hans/docs/pets)。界面名称可能随应用版本变化 / Labels may vary by app version.
