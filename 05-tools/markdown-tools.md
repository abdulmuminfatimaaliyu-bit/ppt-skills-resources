# Markdown工具链 — Markdown转PPT解决方案

## Marp 生态

### Marp CLI
- **项目地址**：[marp-team/marp-cli](https://github.com/marp-team/marp-cli)
- **功能**：将Markdown转换为HTML/PDF/PPTX
- **安装**：`npm install -g @marp-team/marp-cli`

### 使用示例
```bash
# 转换为HTML
marp slide.md -o output.html

# 转换为PDF
marp slide.md --pdf -o output.pdf

# 转换为PPTX
marp slide.md --pptx -o output.pptx

# 实时预览
marp slide.md -w
```

### VS Code集成
- **项目地址**：[marp-team/marp-vscode](https://github.com/marp-team/marp-vscode)
- **功能**：在VS Code中编辑和预览Marp幻灯片
- **安装方式**：VS Code扩展市场搜索"Marp"

## Slidev

### 安装
```bash
npm init slidev@latest
# 或使用CLI
npm install -g @slidev/cli
slidev slides.md
```

### 基本语法
```markdown
---
layout: cover
background: https://source.unsplash.com/collection/94734566/1920x1080
---

# 演示标题

副标题或简介

---

# 内容页

- 要点1
- 要点2
- 要点3

---

# 代码展示

```ts
console.log('Hello Slidev!')
```
```

## md-slides

- **项目地址**：[2aronS/md-slides](https://github.com/2aronS/md-slides)
- **简介**：将Markdown文件转换为演示幻灯片

## 工具推荐总结

| 场景 | 推荐工具 | 优势 |
|------|----------|------|
| 快速制作 | Marp CLI + VS Code | 零学习成本 |
| 技术演示 | Slidev | 代码支持优秀 |
| 批量导出 | Marp CLI | 支持多种格式 |
| Web发布 | Reveal.js | 功能最丰富 |
| 团队协作 | HackMD + hackmd-to-pptx | 在线协作 |
