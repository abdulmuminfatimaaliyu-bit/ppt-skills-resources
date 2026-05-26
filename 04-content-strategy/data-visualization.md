# 数据呈现 — PPT数据可视化指南

## 图表选择指南

### 按数据类型选择

| 数据类型 | 推荐图表 | 用途 |
|----------|----------|------|
| 对比/排名 | 柱状图 | 各品类销售对比 |
| 趋势变化 | 折线图 | 月度业绩走势 |
| 占比分布 | 饼图/圆环图 | 市场份额分配 |
| 相关性 | 散点图 | 投入产出关系 |
| 流程 | 漏斗图 | 转化率分析 |
| 层级 | 树图/旭日图 | 组织结构 |
| 地理 | 地图 | 区域分布 |

## 可视化工具

### Chart.js
- **项目地址**：[chartjs/Chart.js](https://github.com/chartjs/Chart.js)
- **简介**：简单灵活的JavaScript图表库
- **技术栈**：JavaScript, Canvas
- **适用场景**：Web端快速图表展示

### 基本用法
```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [{
      label: '销售额',
      data: [120, 190, 170, 210],
      backgroundColor: 'rgba(54, 162, 235, 0.5)'
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: { display: true, text: '季度销售数据' }
    }
  }
});
```

## 数据呈现原则

### 数据墨水比 (Data-Ink Ratio)
尽量去除不必要的装饰元素，让数据本身说话。

### 图表设计清单
- [ ] 是否有清晰的标题和轴标签？
- [ ] 颜色使用是否合理（色盲友好）？
- [ ] 数据源是否标注？
- [ ] 是否需要网格线？（尽量去掉）
- [ ] 图例是否必要？
- [ ] 是否有误导性比例尺？

## PPT图表实现代码

### 在网页PPT中嵌入图表
```html
<canvas id="myChart" width="400" height="300"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const ctx = document.getElementById('myChart').getContext('2d');
  new Chart(ctx, { /* 配置 */ });
</script>
```

### 使用Canvas绘制简单图表
```javascript
function drawBarChart(ctx, data, width, height) {
  const padding = 40;
  const chartW = width - padding * 2;
  const chartH = height - padding * 2;
  const maxVal = Math.max(...data);
  
  data.forEach((val, i) => {
    const barW = chartW / data.length * 0.7;
    const barH = (val / maxVal) * chartH;
    const x = padding + i * (chartW / data.length) + (chartW / data.length - barW) / 2;
    const y = height - padding - barH;
    
    ctx.fillStyle = '#3498db';
    ctx.fillRect(x, y, barW, barH);
  });
}
```
