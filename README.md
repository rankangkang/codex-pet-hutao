# 胡桃 · Hu Tao

根据头像创作的动画伙伴：圆框眼镜、紫色头发与大胡子、暖黄色上衣和青绿色背带裤。可用于 ChatGPT Work / Pets，也提供 OpenPets 独立桌宠导入包。

![胡桃挥手](assets/previews/waving.gif)

这份项目保存最终宠物图、原始头像、生成的动作条、创作提示词、检查记录，以及本次制作的可复用 Python 工具。

## 用 OpenPets 作为独立桌宠

1. 从 [OpenPets 官方发布页](https://github.com/OpenPetsHQ/openpets/releases)安装适合自己系统的应用。
2. 下载本仓库的 [胡桃 OpenPets 导入包](packages/openpets/hutao-openpets.zip)，保留 ZIP 格式。
3. 打开 OpenPets 控制中心，进入「宠物」→「导入宠物」→「ZIP」，选择这个文件。
4. 在胡桃卡片上点击「设为默认」，关闭控制中心即可在桌面上看到胡桃。

基础桌宠使用无需配置 Codex、其他 Agent、模型或 API key。OpenPets 提供 Windows、macOS 和 Linux 发行版；本仓库目前实测的是 macOS Apple Silicon 上的 OpenPets 4.1.0，已完成本地 ZIP 导入、设为默认、静态缩略图、动画预览和桌面拖动交互检查。未进行 Windows、Linux 或断网启动测试。

试用时在线图库出现 `This operation was aborted`，本地导入和桌宠显示仍成功。具体检查结果见 [试用记录](packages/openpets/smoke-test.json)。

导入包仅包含 `hutao/pet.json` 和 `hutao/spritesheet.webp`。这是已有作品的格式适配：导出无损 WebP，并把第一个待机帧复制到 OpenPets 4.1.0 约定的静止格（从 0 计数的第 0 行、第 6 列），用于静态预览和暂停显示。73 个原始动画帧逐像素保留，`assets/spritesheet.png` 保持原样。布局依据 [OpenPets 4.1.0 源码](https://github.com/OpenPetsHQ/openpets/blob/v4.1.0/apps/desktop/src/codex-pets-core.ts)。

## 动画资源

- `assets/spritesheet.png`：透明 v2 动画图，1536 × 2288，8 列 × 11 行，每格 192 × 208。
- 九组标准动作共 57 帧，加上 16 个顺时针视线方向，共 73 帧；剩余 15 格透明。
- `assets/previews/`：动作 GIF、转头 GIF、静止—跳跃—静止 GIF、关键帧和 MP4。
- `source/rows/`、`references/`、`creation/`：源图、原始头像、创作说明和提示词。
- `qa/`：原始制作流程的检查结果。账号中的宠物 ID 和临时上传链接不属于可移植资源。

## 在本地运行工具

需要 Python 3.10 或更新版本；安装 FFmpeg 后还可输出 MP4。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify_assets.py
python scripts/render_previews.py
```

生成的预览放在 `build/previews/`，不会覆盖已检查的动画图。脚本不需要 OpenAI API key，也不依赖本机安装目录。

重新生成 OpenPets 导入包：

```sh
python scripts/package_openpets.py
```

输出到 `packages/openpets/`，同时生成 [校验报告](packages/openpets/hutao-validation.json)，检查无损编码、变化格子、ZIP 完整性和原图摘要。此导出脚本目前针对本项目的 v2 动画图。

`verify_assets.py` 检查已保存资源的摘要、动画图格式和格子占用；正式导入仍需由 Pets 的上传前检查确认兼容性。新的图像生成和完整宠物创建流程使用 Pets 插件的 create-pet 技能。

`scripts/register_standard_rows.py` 保存了本次制作使用的行内统一缩放和地面位置调整工具。输入是已提取的帧目录及 `frames-manifest.json`，例如：

```sh
python scripts/register_standard_rows.py extracted-frames build/registered-frames
```

## 安装到 ChatGPT Work / Pets

把宠物仓库链接交给装有 Pets 插件的助手，即可下载兼容动画图，检查后导入。私有仓库需要访问该仓库的 GitHub 登录。

对于客户端可直接访问的 HTTPS 动画图，也可以生成官方支持的安装链接：

```sh
python scripts/make_install_link.py --image-url 'https://example.com/spritesheet.png'
```

命令会输出 `codex://pets/install?...&spriteVersionNumber=2`。打开链接后进入桌面客户端的宠物安装流程。请把示例 URL 替换成实际可访问的动画图地址；私有仓库的网页链接通常不能直接作为图片地址。

安装链接格式依据 [OpenAI 官方桌面命令文档](https://learn.chatgpt.com/docs/app/commands#pets)，核实日期为 2026-11-08。

## 保存到 GitHub

项目仓库：[rankangkang/codex-pet-hutao](https://github.com/rankangkang/codex-pet-hutao)。

在其他电脑上获取项目：

```sh
git clone https://github.com/rankangkang/codex-pet-hutao.git
cd codex-pet-hutao
```

在当前仓库提交修改后，使用 `git push -u origin main` 上传。GitHub 登录由本机的 Git 凭据管理器或 `gh auth login` 管理。本项目未附加开源许可。

## 制作记录

最终动画图通过了原制作流程的透明边缘、网格、动作与十六方向检查，以及 Pets 服务的上传前检查。部分斜向视线的变化比较轻微，保留了盲测分歧和后续人工复核记录，详见 `qa/`。

动画图 SHA-256：

```text
2444042e3fd1d23cc47b72589592bf90eaa76d0829bd1e70da39839734cef64b
```
