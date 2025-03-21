import os
from typing import List, Dict, Any, Optional
import logging
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import datetime

from .ai_service_factory import AIServiceFactory

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    生成PDF文档
    """
    def __init__(self, ai_service_type: str = "deepseek"):
        # 使用绝对路径
        self.output_dir = os.path.abspath("generated_docs")
        logger.info(f"PDF生成器输出目录: {self.output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 确保目录权限正确
        try:
            os.chmod(self.output_dir, 0o777)
        except Exception as e:
            logger.warning(f"无法修改目录权限: {e}")
            
        self.ai_service = AIServiceFactory.create_service(ai_service_type)
    
    def generate(self, topic: str, outline: List[Dict[str, Any]], template_id: Optional[str] = None) -> Optional[str]:
        """
        根据大纲生成PDF文档
        
        Args:
            topic: 文档主题
            outline: 文档大纲
            template_id: 可选的模板ID
            
        Returns:
            生成的PDF文件路径，如果失败则返回None
        """
        try:
            logger.info(f"开始生成PDF文档: 主题='{topic}', 章节数={len(outline)}")
            if template_id:
                logger.info(f"使用模板: {template_id}")
            
            # 创建文件名和文档
            file_name = f"{topic.replace(' ', '_')}_document.pdf"
            file_path = os.path.join(self.output_dir, file_name)
            
            # 创建文档对象
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            logger.info(f"创建新的PDF文档对象，页面大小: {letter}")
            
            # 获取样式
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='Title',
                parent=styles['Heading1'],
                fontSize=24,
                alignment=TA_CENTER,
                spaceAfter=36
            ))
            styles.add(ParagraphStyle(
                name='Normal_Justified',
                parent=styles['Normal'],
                alignment=TA_JUSTIFY,
                fontSize=12,
                leading=14,
                spaceAfter=12
            ))
            
            # 创建内容元素列表
            elements = []
            
            # 添加标题页
            logger.info("添加标题页")
            elements.append(Paragraph(topic, styles['Title']))
            elements.append(Paragraph("AI自动生成的文档", styles['Heading2']))
            elements.append(Spacer(1, 0.5*inch))
            elements.append(Paragraph(datetime.datetime.now().strftime("%Y年%m月%d日"), styles['Normal']))
            elements.append(PageBreak())
            
            # 添加目录
            logger.info("添加目录")
            elements.append(Paragraph("目录", styles['Heading1']))
            elements.append(Spacer(1, 0.25*inch))
            
            for i, section in enumerate(outline):
                section_title = section.get("title", "未知章节")
                elements.append(Paragraph(f"{i+1}. {section_title}", styles['Normal']))
                
                # 添加子章节到目录
                subsections = section.get("subsections", [])
                for j, subsection in enumerate(subsections):
                    subsection_title = subsection.get("title", "未知子章节")
                    elements.append(Paragraph(f"   {i+1}.{j+1} {subsection_title}", styles['Normal']))
            
            elements.append(PageBreak())
            
            # 添加章节内容
            for section_index, section in enumerate(outline):
                section_title = section.get("title", "未知章节")
                logger.info(f"处理章节 {section_index+1}/{len(outline)}: '{section_title}'")
                
                # 添加章节标题
                elements.append(Paragraph(f"{section_index+1}. {section_title}", styles['Heading1']))
                
                # 生成章节内容
                content = self.ai_service.generate_section_content(topic, section_title, "pdf")
                paragraphs = content.strip().split('\n\n')
                for p_text in paragraphs:
                    if p_text:
                        elements.append(Paragraph(p_text.strip(), styles['Normal_Justified']))
                
                # 处理子章节
                subsections = section.get("subsections", [])
                if subsections:
                    logger.info(f"  章节 '{section_title}' 包含 {len(subsections)} 个子章节")
                    
                    for subsection_index, subsection in enumerate(subsections):
                        subsection_title = subsection.get("title", "未知子章节")
                        logger.info(f"    处理子章节 {subsection_index+1}/{len(subsections)}: '{subsection_title}'")
                        
                        # 添加子章节标题
                        elements.append(Paragraph(
                            f"{section_index+1}.{subsection_index+1} {subsection_title}", 
                            styles['Heading2']
                        ))
                        
                        # 生成子章节内容
                        subcontent = self.ai_service.generate_section_content(topic, subsection_title, "pdf")
                        subparagraphs = subcontent.strip().split('\n\n')
                        for p_text in subparagraphs:
                            if p_text:
                                elements.append(Paragraph(p_text.strip(), styles['Normal_Justified']))
            
            # 添加参考文献
            logger.info("添加参考文献")
            elements.append(PageBreak())
            elements.append(Paragraph("参考文献", styles['Heading1']))
            elements.append(Spacer(1, 0.25*inch))
            
            # 生成一些模拟的参考文献
            references = [
                f"[1] AI文档生成系统. (2023). {topic}研究综述.",
                f"[2] 智能文档分析小组. (2023). {topic}的最新进展.",
                f"[3] 文档自动化协会. (2022). {topic}标准与实践."
            ]
            
            for ref in references:
                elements.append(Paragraph(ref, styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
            
            # 构建文档
            logger.info("构建PDF文档")
            doc.build(elements)
            
            # 估算页数
            page_count = len(elements) // 20  # 假设每页约20个元素
            logger.info(f"PDF文档生成成功: 约 {page_count} 页, 保存至: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"生成PDF文档时出错: {str(e)}")
            return None 