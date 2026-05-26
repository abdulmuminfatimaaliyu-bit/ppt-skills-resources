# Web框架工具 — 基于Web的PPT制作

## Reveal.js

- **项目地址**：[https://github.com/hakimel/reveal.js](https://github.com/hakimel/reveal.js)
- **简介**：业界最流行的HTML演示框架
- **Star数**：74k+
- **技术栈**：HTML/CSS/JavaScript
- **许可**：MIT

### 快速开始
```bash
npm install reveal.js
```

### 核心配置
```javascript
Reveal.initialize({
  controls: true,
  progress: true,
  slideNumber: true,
  hash: true,
  transition: 'slide',
  plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ]
});
```

## Slidev

- **项目地址**：[https://github.com/slidevjs/slidev](https://github.com/slidevjs/slidev)
- **简介**：面向开发者的演示文稿制作工具
- **技术栈**：Vue.js + Vite + Markdown
- **许可**：MIT

### 安装
```bash
npm init slidev@latest
```

### 特性
- 基于Markdown的幻灯片编写
- 代码实时预览
- 主题系统
- 录音功能
- 导出PDF/PPTX

## 工具选择指南

| 需求 | 推荐工具 | 理由 |
|------|----------|------|
| 技术演讲 | Reveal.js | 代码高亮、LaTeX支持 |
| 快速制作 | Marp | Markdown即幻灯片 |
| 交互式演示 | Spectacle | React组件化 |
| 在线分享 | Slidev | 一键部署 |
| 导出PPTX | PptxGenJS | 原生PPTX格式 |
