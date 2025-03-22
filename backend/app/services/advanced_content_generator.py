import logging
from typing import Dict, Any, List, Optional, Tuple, Callable
import json
from pydantic import ValidationError
import re

from .ai_service_factory import AIServiceFactory
from .outline_generator import OutlineGenerator
from ..models.schemas import PageChapterContent

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedContentGenerator:
    def __init__(self, ai_service_type: str = "deepseek"):
        self.ai_service = AIServiceFactory.create_service(ai_service_type)
        self.outline_generator = OutlineGenerator(self.ai_service)
        logger.info(f"高级内容生成器已初始化，使用 {ai_service_type} 服务")
    
    async def generate_with_constraints(
        self, 
        topic: str, 
        doc_type: str, 
        additional_info: Optional[str] = None,
        max_pages: Optional[int] = None,
        detailed_content: Optional[List[PageChapterContent]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """
        根据用户提供的约束生成内容
        
        Args:
            topic: 文档主题
            doc_type: 文档类型 (ppt 或 word)
            additional_info: 附加信息
            max_pages: 限制最大页数/章节数
            detailed_content: 用户定义的具体页面/章节内容
            progress_callback: 进度回调函数
            
        Returns:
            包含大纲和详细内容的字典
        """
        try:
            logger.info(f"开始高级模式内容生成: 主题='{topic}', 类型={doc_type}")
            if max_pages:
                logger.info(f"应用页数/章节限制: {max_pages}")
            if detailed_content:
                logger.info(f"用户提供了 {len(detailed_content)} 个自定义页面/章节")
            
            # 步骤1: 生成基本大纲
            if progress_callback:
                progress_callback(0.1, "正在生成基本大纲...")
            
            # 如果用户提供了详细内容，我们构建基于这些内容的大纲
            if detailed_content and len(detailed_content) > 0:
                outline = self._build_outline_from_user_content(
                    topic, 
                    doc_type, 
                    detailed_content,
                    max_pages
                )
                logger.info("基于用户提供的内容创建了大纲")
            else:
                # 否则通过AI生成大纲
                outline_constraints = ""
                if max_pages:
                    outline_constraints = f"大纲必须限制在最多{max_pages}个{'页面' if doc_type == 'ppt' else '章节'}内。"
                
                outline = await self._generate_ai_outline(
                    topic, 
                    doc_type, 
                    f"{additional_info or ''} {outline_constraints}".strip()
                )
                logger.info("通过AI生成了大纲")
            
            if progress_callback:
                progress_callback(0.3, "大纲生成完成，开始生成详细内容...")
            
            # 步骤2: 填充详细内容
            full_content = await self._generate_detailed_content(
                topic,
                doc_type,
                outline,
                detailed_content,
                progress_callback
            )
            
            if progress_callback:
                progress_callback(0.95, "内容生成完成，准备导出...")
            
            logger.info(f"高级内容生成完成，主题: {topic}")
            return full_content
            
        except Exception as e:
            logger.error(f"高级内容生成错误: {str(e)}")
            raise
    
    def _build_outline_from_user_content(
        self, 
        topic: str, 
        doc_type: str, 
        user_content: List[PageChapterContent],
        max_pages: Optional[int] = None
    ) -> Dict[str, Any]:
        """根据用户提供的内容构建大纲"""
        # 按位置排序用户内容
        sorted_content = sorted(user_content, key=lambda x: x.position)
        
        # 如果有最大页数限制，确保不超过
        if max_pages and len(sorted_content) > max_pages:
            logger.info(f"用户内容超过最大限制({max_pages})，将截断至{max_pages}个条目")
            sorted_content = sorted_content[:max_pages]
        
        if doc_type == "ppt":
            # 创建PPT大纲
            sections = []
            current_section = {
                "title": "主要内容",
                "slides": []
            }
            
            # 确保幻灯片数量不超过max_pages
            total_slides = 0
            for item in sorted_content:
                # 计数标题和结束幻灯片
                base_slides = 2  # 标题幻灯片和结束幻灯片
                if max_pages and total_slides + len(current_section["slides"]) + base_slides >= max_pages:
                    # 如果已经达到限制，不再添加更多幻灯片
                    logger.info(f"已达到幻灯片数量限制({max_pages})，停止添加更多内容")
                    break
                
                current_section["slides"].append({
                    "title": item.title,
                    "content": item.content or f"关于{item.title}的内容",
                    "type": "content"
                })
            
            sections.append(current_section)
            
            # 记录最终大纲信息
            total_slides = base_slides + sum(len(section.get("slides", [])) for section in sections)
            logger.info(f"构建的PPT大纲包含 {total_slides} 张幻灯片，最大限制为 {max_pages or '无限制'}")
            
            return {
                "title": topic,
                "sections": sections
            }
        else:
            # 创建Word大纲
            sections = []
            for item in sorted_content:
                # 如果已达到章节数限制，停止添加
                if max_pages and len(sections) >= max_pages:
                    logger.info(f"已达到章节数量限制({max_pages})，停止添加更多内容")
                    break
                    
                sections.append({
                    "title": item.title,
                    "content": item.content or f"关于{item.title}的内容",
                    "subsections": []
                })
            
            logger.info(f"构建的Word大纲包含 {len(sections)} 章节，最大限制为 {max_pages or '无限制'}")
            
            return {
                "title": topic,
                "sections": sections
            }
    
    async def _generate_detailed_content(
        self,
        topic: str,
        doc_type: str,
        outline: Dict[str, Any],
        user_content: Optional[List[PageChapterContent]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """根据大纲填充详细内容"""
        # 创建用户内容的映射表，以便快速查找
        user_content_map = {}
        if user_content:
            for item in user_content:
                user_content_map[item.title] = item.content
        
        # 检查大纲中的章节/幻灯片数量
        if doc_type == "ppt":
            total_slides = 2  # 标题和结束幻灯片
            for section in outline.get("sections", []):
                total_slides += 1  # 章节标题幻灯片
                total_slides += len(section.get("slides", []))
            logger.info(f"生成详细内容: PPT共计 {total_slides} 张幻灯片")
            
            # 处理PPT内容
            result = {"title": outline["title"], "sections": []}
            
            for section_idx, section in enumerate(outline["sections"]):
                # 计算总体进度
                if progress_callback:
                    progress_percent = 0.3 + 0.65 * (section_idx / len(outline["sections"]))
                    progress_callback(progress_percent, f"正在生成第 {section_idx+1}/{len(outline['sections'])} 章节...")
                
                # 复制章节基本信息
                result_section = {
                    "title": section["title"],
                    "slides": []
                }
                
                # 处理每个幻灯片
                for slide in section.get("slides", []):
                    # 如果用户提供了这个标题的内容，使用用户内容
                    if slide["title"] in user_content_map and user_content_map[slide["title"]]:
                        # 可以根据需要转换用户内容格式
                        logger.info(f"使用用户提供的内容: {slide['title']}")
                        slide["content"] = user_content_map[slide["title"]]
                    
                    result_section["slides"].append(slide)
                
                result["sections"].append(result_section)
            
            # 最终记录生成的内容大小
            final_total_slides = 2  # 标题和结束幻灯片
            for section in result["sections"]:
                final_total_slides += 1  # 章节标题幻灯片
                final_total_slides += len(section.get("slides", []))
            logger.info(f"完成PPT内容生成: 共计 {final_total_slides} 张幻灯片")
            
            return result
        else:
            # 处理Word内容
            total_sections = len(outline.get("sections", []))
            logger.info(f"生成详细内容: Word文档共计 {total_sections} 个章节")
            
            result = {"title": outline["title"], "sections": []}
            
            for section_idx, section in enumerate(outline["sections"]):
                # 计算总体进度
                if progress_callback:
                    progress_percent = 0.3 + 0.65 * (section_idx / total_sections)
                    progress_callback(progress_percent, f"正在生成第 {section_idx+1}/{total_sections} 章节...")
                
                # 如果用户提供了这个标题的内容，使用用户内容
                if section["title"] in user_content_map and user_content_map[section["title"]]:
                    section["content"] = user_content_map[section["title"]]
                    logger.info(f"使用用户提供的内容: {section['title']}")
                # 否则进行内容填充
                elif not section.get("content"):
                    # 这里可以添加AI内容生成
                    # 为了简化，这里只使用占位符
                    section["content"] = f"关于{section['title']}的详细内容"
                
                result["sections"].append(section)
            
            # 最终记录生成的内容大小
            logger.info(f"完成Word内容生成: 共计 {len(result['sections'])} 个章节")
            
            return result
    
    async def _generate_ai_outline(
        self, 
        topic: str, 
        doc_type: str, 
        additional_info: str = ""
    ) -> Dict[str, Any]:
        """
        使用AI生成文档大纲
        
        Args:
            topic: 文档主题
            doc_type: 文档类型 (ppt 或 word)
            additional_info: 附加信息
            
        Returns:
            大纲字典
        """
        try:
            logger.info(f"使用AI生成大纲: 主题={topic}, 类型={doc_type}")
            
            # 从additional_info中提取max_pages约束
            max_pages = None
            if "大纲必须限制在最多" in additional_info and "个" in additional_info:
                try:
                    # 尝试提取数字
                    match = re.search(r'大纲必须限制在最多(\d+)个', additional_info)
                    if match:
                        max_pages = int(match.group(1))
                        logger.info(f"从附加信息中提取到页数限制: {max_pages}")
                except ValueError:
                    logger.warning("无法从附加信息中提取页数限制")
            
            # 使用AI服务生成大纲
            sections = self.outline_generator.generate_document_outline(topic, doc_type)
            
            if not sections:
                # 如果AI生成失败，创建一个基本大纲
                logger.warning(f"AI生成大纲失败，创建基本大纲: {topic}")
                
                if doc_type == "ppt":
                    # 为PPT创建基本大纲
                    basic_outline = {
                        "title": topic,
                        "sections": [
                            {
                                "title": "概述",
                                "slides": [
                                    {"title": f"{topic}简介", "type": "content"},
                                    {"title": "主要内容", "type": "content"},
                                    {"title": "关键点", "type": "content"},
                                ]
                            },
                            {
                                "title": "详细内容",
                                "slides": [
                                    {"title": f"{topic}的基本概念", "type": "content"},
                                    {"title": "重要特性", "type": "content"},
                                    {"title": "应用场景", "type": "content"},
                                ]
                            },
                            {
                                "title": "总结",
                                "slides": [
                                    {"title": "主要收获", "type": "content"},
                                    {"title": "未来展望", "type": "content"},
                                ]
                            }
                        ]
                    }
                    
                    # 应用最大页数限制
                    if max_pages:
                        # 计算当前幻灯片总数
                        total_slides = 2  # 标题幻灯片和结束幻灯片
                        for section in basic_outline["sections"]:
                            total_slides += 1  # 每个章节有一张章节标题幻灯片
                            total_slides += len(section.get("slides", []))
                        
                        # 如果超出限制，逐步减少内容
                        if total_slides > max_pages:
                            logger.info(f"基本大纲超过页数限制({max_pages})，进行裁剪")
                            
                            # 保留概述和总结章节，删除/缩减中间章节
                            if len(basic_outline["sections"]) > 2:
                                # 保留第一个和最后一个章节
                                basic_outline["sections"] = [basic_outline["sections"][0], basic_outline["sections"][-1]]
                            
                            # 如果还是太多，继续减少幻灯片
                            total_slides = 2  # 重新计算
                            for section in basic_outline["sections"]:
                                total_slides += 1  # 章节标题幻灯片
                                total_slides += len(section.get("slides", []))
                            
                            if total_slides > max_pages:
                                # 每个章节最多保留一张幻灯片
                                for section in basic_outline["sections"]:
                                    if len(section.get("slides", [])) > 1:
                                        section["slides"] = section["slides"][:1]
                    
                    return basic_outline
                else:
                    # 为Word文档创建基本大纲
                    basic_outline = {
                        "title": topic,
                        "sections": [
                            {
                                "title": "引言",
                                "subsections": [
                                    {"title": f"{topic}背景"},
                                    {"title": "研究意义"}
                                ]
                            },
                            {
                                "title": "理论基础",
                                "subsections": [
                                    {"title": "基本概念"},
                                    {"title": "核心原理"}
                                ]
                            },
                            {
                                "title": "应用与实践",
                                "subsections": [
                                    {"title": "典型应用"},
                                    {"title": "案例分析"}
                                ]
                            },
                            {
                                "title": "总结与展望",
                                "subsections": [
                                    {"title": "主要成果"},
                                    {"title": "未来研究方向"}
                                ]
                            }
                        ]
                    }
                    
                    # 应用最大章节数限制
                    if max_pages and len(basic_outline["sections"]) > max_pages:
                        logger.info(f"基本大纲超过章节限制({max_pages})，进行裁剪")
                        # 保留必要的章节，如引言和总结
                        if max_pages >= 2:
                            basic_outline["sections"] = [basic_outline["sections"][0]] + basic_outline["sections"][-(max_pages-1):]
                        else:
                            basic_outline["sections"] = basic_outline["sections"][:max_pages]
                    
                    return basic_outline
            
            # 如果AI生成成功，构建完整大纲并应用页数限制
            outline = {
                "title": topic,
                "sections": sections
            }
            
            # 应用最大页数限制
            if max_pages:
                if doc_type == "ppt":
                    # 计算当前幻灯片总数
                    total_slides = 2  # 标题幻灯片和结束幻灯片
                    for section in outline["sections"]:
                        total_slides += 1  # 每个章节有一张章节标题幻灯片
                        total_slides += len(section.get("slides", []))
                    
                    # 如果超出限制，逐步减少内容
                    if total_slides > max_pages:
                        logger.info(f"AI生成的大纲超过页数限制({max_pages})，当前页数{total_slides}，进行裁剪")
                        
                        # 从最后一个章节开始减少内容
                        removed_slides = 0
                        for i in range(len(outline["sections"])-1, -1, -1):
                            section = outline["sections"][i]
                            while len(section.get("slides", [])) > 0 and total_slides > max_pages:
                                section["slides"].pop()
                                total_slides -= 1
                                removed_slides += 1
                            
                            # 如果章节内容为空，考虑移除整个章节
                            if len(section.get("slides", [])) == 0 and len(outline["sections"]) > 1:
                                outline["sections"].pop(i)
                                total_slides -= 1  # 减去章节标题幻灯片
                                removed_slides += 1
                            
                            if total_slides <= max_pages:
                                break
                        
                        logger.info(f"裁剪完成，移除了{removed_slides}个内容，调整后页数为{total_slides}")
                else:
                    # 对Word文档应用章节数限制
                    if len(outline["sections"]) > max_pages:
                        logger.info(f"AI生成的大纲超过章节限制({max_pages})，进行裁剪")
                        # 保留有意义的章节（如开头和结尾）
                        if max_pages >= 2:
                            outline["sections"] = outline["sections"][:max_pages-1] + [outline["sections"][-1]]
                        else:
                            outline["sections"] = outline["sections"][:max_pages]
            
            return outline
        
        except Exception as e:
            logger.error(f"生成大纲时出错: {str(e)}")
            # 发生错误时返回一个最小大纲
            return {
                "title": topic,
                "sections": [{"title": "主要内容", "slides" if doc_type == "ppt" else "subsections": []}]
            }