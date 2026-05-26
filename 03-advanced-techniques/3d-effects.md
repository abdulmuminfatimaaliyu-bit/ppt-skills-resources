# 3D效果在PPT中的应用

## CSS 3D变换

### 基础3D变换
```css
.perspective-container {
  perspective: 1000px;
}

.card-3d {
  transform: rotateX(10deg) rotateY(20deg);
  transform-style: preserve-3d;
  transition: transform 0.5s ease;
}

.card-3d:hover {
  transform: rotateX(0deg) rotateY(0deg) scale(1.05);
}
```

### 3D翻转效果
```css
.flip-card {
  perspective: 1000px;
}

.flip-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card:hover .flip-inner {
  transform: rotateY(180deg);
}

.flip-front, .flip-back {
  backface-visibility: hidden;
  position: absolute;
}

.flip-back {
  transform: rotateY(180deg);
}
```

## Canvas 3D图表

### 3D柱状图示例
```javascript
const canvas = document.getElementById('chart');
const ctx = canvas.getContext('2d');

function draw3DBar(ctx, x, y, width, height, depth, color) {
  // 正面
  ctx.fillStyle = color;
  ctx.fillRect(x, y - height, width, height);
  
  // 顶面
  ctx.fillStyle = lighten(color, 30);
  ctx.beginPath();
  ctx.moveTo(x, y - height);
  ctx.lineTo(x + depth * 0.5, y - height - depth * 0.5);
  ctx.lineTo(x + width + depth * 0.5, y - height - depth * 0.5);
  ctx.lineTo(x + width, y - height);
  ctx.closePath();
  ctx.fill();
  
  // 侧面
  ctx.fillStyle = darken(color, 20);
  ctx.beginPath();
  ctx.moveTo(x + width, y - height);
  ctx.lineTo(x + width + depth * 0.5, y - height - depth * 0.5);
  ctx.lineTo(x + width + depth * 0.5, y - depth * 0.5);
  ctx.lineTo(x + width, y);
  ctx.closePath();
  ctx.fill();
}
```

## 3D展示工具

| 工具 | 用途 | 适用平台 |
|------|------|----------|
| Three.js | 3D场景渲染 | Web |
| CSS 3D变换 | 卡片/翻转效果 | Web |
| Canvas 2.5D | 伪3D图表 | Web |

## 性能注意事项
- GPU加速：使用 `transform: translateZ(0)` 触发
- 减少重绘：使用 `requestAnimationFrame`
- 限制3D元素数量：不超过10-15个
- 移动端注意：降低渲染复杂度
