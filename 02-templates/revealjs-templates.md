# Reveal.js 模板资源

## 核心框架

### Reveal.js
- **项目地址**：[hakimel/reveal.js](https://github.com/hakimel/reveal.js)
- **Star数**：74k+
- **简介**：HTML演示框架，支持Markdown、LaTeX、代码高亮
- **技术栈**：HTML/CSS/JavaScript
- **适用场景**：技术演讲、在线演示、交互式展示

### 核心特性
- 嵌套幻灯片（垂直+水平）
- Markdown支持
- 代码语法高亮
- LaTeX数学公式
- 演讲者笔记
- 自动动画
- 导出PDF
- 触摸导航

## 主题资源

### Swiss Design 主题
- **项目地址**：[mirdaki/revealjs-swiss](https://github.com/mirdaki/revealjs-swiss)
- **简介**：瑞士设计风格的主题集合
- **风格**：简洁、现代、国际化

### TU Eindhoven 主题
- **项目地址**：[FerryT/TU-Eindhoven-Reveal.js-Theme](https://github.com/FerryT/TU-Eindhoven-Reveal.js-Theme)
- **简介**：埃因霍温理工大学非官方Reveal.js主题

## 扩展插件

### Reveal.js MQTT 插件
- **项目地址**：[roccomuso/reveal.js-mqtt-plugin](https://github.com/roccomuso/reveal.js-mqtt-plugin)
- **功能**：通过MQTT实现多屏同步演示

## 工具集成

### Rayveal
- **项目地址**：[planetoftheweb/rayveal](https://github.com/planetoftheweb/rayveal)
- **简介**：以Markdown为先的演示框架，基于Reveal.js
- **特性**：预装插件、Bootstrap集成

### Reveal JS Editor
- **项目地址**：[fbedussi/reveal-js-editor](https://github.com/fbedussi/reveal-js-editor)
- **简介**：基于Electron的跨平台编辑器，用Markdown创作Reveal.js演示

## 快速上手

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js/dist/theme/black.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section>幻灯片 1</section>
      <section>幻灯片 2</section>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js/dist/reveal.js"></script>
  <script>Reveal.initialize();</script>
</body>
</html>
```
