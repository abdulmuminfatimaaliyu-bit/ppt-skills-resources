# Python自动化工具

## python-pptx

- **官方文档**：[python-pptx.readthedocs.io](https://python-pptx.readthedocs.io/)
- **简介**：创建和修改PowerPoint文件的Python库
- **安装**：`pip install python-pptx`
- **许可**：MIT

### 基础示例
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "我的演示文稿"

# 添加文本框
from pptx.util import Inches, Pt
left = Inches(1)
top = Inches(2)
width = Inches(8)
height = Inches(4)
textbox = slide.shapes.add_textbox(left, top, width, height)
tf = textbox.text_frame
tf.text = "这是正文内容"

prs.save('output.pptx')
```

### 插入图表
```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Sales', (120, 190, 170, 210))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(1), Inches(2), Inches(8), Inches(5),
    chart_data
).chart
```

## 相关项目

| 项目 | 链接 | 说明 |
|------|------|------|
| automate-powerpoint | [GitHub](https://github.com/samirsaci/automate-powerpoint) | 使用Python自动化创建PPT |
| easypptx | [GitHub](https://github.com/Ameyanagi/easypptx) | 简单的PPT操作库 |
| PowerPoint-Generator-Using-Gemini-AI | [GitHub](https://github.com/abhijiths19/PowerPoint-Generator-Using-Gemini-AI) | AI驱动PPT生成 |
| excel-powerpoint-demo | [GitHub](https://github.com/jrmistry/excel-powerpoint-demo) | Excel数据填充PPT示例 |
