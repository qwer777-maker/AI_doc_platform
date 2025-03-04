from typing import Dict, Any, Optional, List
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from ..core.config import settings
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PPTGenerator:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), "../templates/ppt_templates")
        self.output_dir = "generated_docs"  # 输出目录
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate(self, topic: str, outline: List[Dict[str, Any]], template_id: Optional[str] = None) -> Optional[str]:
        """
        根据大纲生成PPT文档
        
        Args:
            topic: 文档主题
            outline: 文档大纲
            template_id: 可选的模板ID
            
        Returns:
            生成的PPT文件路径，如果失败则返回None
        """
        try:
            logger.info(f"开始生成PPT: {topic}")
            
            # 创建演示文稿
            prs = self._create_presentation(template_id)
            
            # 添加标题幻灯片
            self._add_title_slide(prs, topic)
            
            # 添加目录幻灯片
            self._add_toc_slide(prs, outline)
            
            # 添加内容幻灯片
            for section in outline:
                self._add_section_slides(prs, section, topic)
            
            # 添加结束幻灯片
            self._add_ending_slide(prs, topic)
            
            # 保存文件
            file_name = f"{topic.replace(' ', '_')}_presentation.pptx"
            file_path = os.path.join(self.output_dir, file_name)
            prs.save(file_path)
            
            logger.info(f"PPT生成成功: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"生成PPT时出错: {str(e)}")
            return None
    
    def _create_presentation(self, template_id: Optional[str]) -> Presentation:
        """
        创建演示文稿对象，可选择使用模板
        """
        # 如果提供了模板ID，尝试加载模板
        if template_id and template_id != "default":
            template_path = f"templates/ppt/{template_id}.pptx"
            if os.path.exists(template_path):
                return Presentation(template_path)
        
        # 默认创建空白演示文稿
        return Presentation()
    
    def _add_title_slide(self, prs: Presentation, topic: str) -> None:
        """
        添加标题幻灯片
        """
        slide_layout = prs.slide_layouts[0]  # 使用标题布局
        slide = prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = topic
        subtitle.text = "AI自动生成的演示文稿"
        
        # 设置标题样式
        for paragraph in title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(44)
                run.font.bold = True
                run.font.color.rgb = RGBColor(44, 62, 80)
        
        # 设置副标题样式
        for paragraph in subtitle.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(24)
                run.font.italic = True
                run.font.color.rgb = RGBColor(52, 73, 94)
    
    def _add_toc_slide(self, prs: Presentation, outline: List[Dict[str, Any]]) -> None:
        """
        添加目录幻灯片
        """
        slide_layout = prs.slide_layouts[1]  # 使用标题和内容布局
        slide = prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = "目录"
        
        # 添加目录内容
        tf = content.text_frame
        for i, section in enumerate(outline, 1):
            p = tf.add_paragraph()
            p.text = f"{i}. {section['title']}"
            p.level = 0
            
            # 设置段落样式
            p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.size = Pt(24)
                run.font.bold = True
                run.font.color.rgb = RGBColor(41, 128, 185)
    
    def _add_section_slides(self, prs: Presentation, section: Dict[str, Any], topic: str) -> None:
        """
        添加章节幻灯片
        """
        # 添加章节标题幻灯片
        slide_layout = prs.slide_layouts[2]  # 使用章节标题布局
        slide = prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        title.text = section["title"]
        
        # 设置标题样式
        for paragraph in title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(40)
                run.font.bold = True
                run.font.color.rgb = RGBColor(41, 128, 185)
        
        # 添加章节内容幻灯片
        slides = section.get("slides", [])
        if not slides:
            # 如果没有指定幻灯片，创建一个默认幻灯片
            self._add_default_content_slide(prs, section["title"], topic)
            return
        
        for slide_info in slides:
            self._add_content_slide(prs, slide_info, section["title"], topic)
    
    def _add_content_slide(self, prs: Presentation, slide_info: Dict[str, Any], section_title: str, topic: str) -> None:
        """
        添加内容幻灯片
        """
        slide_layout = prs.slide_layouts[1]  # 使用标题和内容布局
        slide = prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = slide_info["title"]
        
        # 设置标题样式
        for paragraph in title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.LEFT
            for run in paragraph.runs:
                run.font.size = Pt(32)
                run.font.bold = True
                run.font.color.rgb = RGBColor(52, 73, 94)
        
        # 添加模拟内容
        tf = content.text_frame
        
        # 这里可以调用AI服务生成实际内容
        # 现在使用模拟内容
        bullet_points = [
            f"{slide_info['title']}是{topic}的重要组成部分",
            f"它包含多个关键要素和特性",
            f"理解{slide_info['title']}对掌握{section_title}至关重要",
            f"未来发展趋势将进一步强化其重要性"
        ]
        
        for point in bullet_points:
            p = tf.add_paragraph()
            p.text = point
            p.level = 0
            
            # 设置段落样式
            p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.size = Pt(24)
                run.font.color.rgb = RGBColor(44, 62, 80)
    
    def _add_default_content_slide(self, prs: Presentation, section_title: str, topic: str) -> None:
        """
        添加默认内容幻灯片
        """
        slide_layout = prs.slide_layouts[1]  # 使用标题和内容布局
        slide = prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = f"{section_title} - 关键要点"
        
        # 设置标题样式
        for paragraph in title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.LEFT
            for run in paragraph.runs:
                run.font.size = Pt(32)
                run.font.bold = True
                run.font.color.rgb = RGBColor(52, 73, 94)
        
        # 添加模拟内容
        tf = content.text_frame
        
        bullet_points = [
            f"{section_title}是{topic}的核心组成部分",
            f"它包含多个关键要素和特性",
            f"深入理解{section_title}对掌握整个主题至关重要",
            f"未来研究将进一步探索其潜力和应用"
        ]
        
        for point in bullet_points:
            p = tf.add_paragraph()
            p.text = point
            p.level = 0
            
            # 设置段落样式
            p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.size = Pt(24)
                run.font.color.rgb = RGBColor(44, 62, 80)
    
    def _add_ending_slide(self, prs: Presentation, topic: str) -> None:
        """
        添加结束幻灯片
        """
        slide_layout = prs.slide_layouts[1]  # 使用标题和内容布局
        slide = prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = "总结与问答"
        
        # 设置标题样式
        for paragraph in title.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(40)
                run.font.bold = True
                run.font.color.rgb = RGBColor(41, 128, 185)
        
        # 添加总结内容
        tf = content.text_frame
        
        summary_points = [
            f"我们探讨了{topic}的多个关键方面",
            f"理解这些概念对把握{topic}的本质至关重要",
            f"未来发展将带来更多机遇和挑战",
            f"感谢您的关注！有任何问题欢迎提问"
        ]
        
        for point in summary_points:
            p = tf.add_paragraph()
            p.text = point
            p.level = 0
            
            # 设置段落样式
            p.alignment = PP_ALIGN.CENTER
            for run in p.runs:
                run.font.size = Pt(28)
                run.font.color.rgb = RGBColor(44, 62, 80) 