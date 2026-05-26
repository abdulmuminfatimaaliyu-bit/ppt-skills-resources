# 动画框架与效果实现

## Reveal.js 动画系统

### 内置动画
```javascript
// 进入动画
<section data-transition="fade">淡入</section>
<section data-transition="slide">滑入</section>
<section data-transition="convex">凸入</section>
<section data-transition="concave">凹入</section>
<section data-transition="zoom">缩放</section>

// 自动动画（Reveal.js 4.x+）
<section data-auto-animate>
  <h1>原始标题</h1>
</section>
<section data-auto-animate>
  <h1 style="color: red;">动画后标题</h1>
</section>
```

### 高级动画配置
```javascript
Reveal.initialize({
  autoAnimate: true,
  autoAnimateEasing: 'ease-out',
  autoAnimateDuration: 1.0,
  autoAnimateUnmatched: true
});
```

## Framer Motion (React动画库)
- **项目地址**：[framer/motion](https://github.com/framer/motion)
- **适用场景**：React演示文稿中的精细动画控制

### 基本示例
```jsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 50 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  动画内容
</motion.div>
```

## CSS动画在PPT中的应用

### 关键帧动画
```css
@keyframes slideIn {
  from { transform: translateX(-100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.slide-element {
  animation: slideIn 0.8s ease-out forwards;
}
```

### 过渡效果
```css
.element {
  transition: all 0.3s ease;
}
.element:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}
```

## 性能优化建议
- 使用 `transform` 和 `opacity` 实现动画（GPU加速）
- 避免对 `width`、`height`、`top`、`left` 做动画
- 合理使用 `will-change` 属性
- 控制同时播放的动画数量（不超过3-5个）
