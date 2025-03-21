import logging
from typing import Dict, Any, Optional, List

from .ai_client import AIClient

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    """
    文档内容生成器
    """
    
    def __init__(self, ai_client: AIClient):
        """
        初始化内容生成器
        
        Args:
            ai_client: AI客户端实例
        """
        self.ai_client = ai_client
        logger.info("内容生成器初始化完成")
    
    def generate_section_content(self, topic: str, section_title: str, doc_type: str) -> str:
        """
        生成文档章节内容
        
        Args:
            topic: 文档主题
            section_title: 章节标题
            doc_type: 文档类型 (ppt, word, pdf)
            
        Returns:
            章节内容
        """
        try:
            logger.info(f"开始为章节 '{section_title}' 生成内容 (主题: {topic}, 类型: {doc_type})")
            
            # 构建提示
            prompt = self._build_section_prompt(topic, section_title, doc_type)
            
            # 调用AI客户端
            messages = [
                {"role": "system", "content": "你是一个专业的文档内容生成助手，擅长创建高质量、信息丰富的文档内容。"},
                {"role": "user", "content": prompt}
            ]
            
            response = self.ai_client.call_api(messages)
            
            if not response:
                logger.warning(f"生成章节 '{section_title}' 内容失败，使用模拟内容")
                return self._get_mock_section_content(topic, section_title)
            
            # 提取内容
            content = self.ai_client.extract_response_content(response)
            
            if not content:
                logger.warning(f"从响应中提取章节 '{section_title}' 内容失败，使用模拟内容")
                return self._get_mock_section_content(topic, section_title)
            
            # 记录生成的内容摘要
            content_preview = content.replace('\n', ' ')[:100] + "..." if len(content) > 100 else content
            logger.info(f"成功生成章节 '{section_title}' 内容: {content_preview}")
            
            return content
            
        except Exception as e:
            logger.error(f"生成章节内容时出错: {str(e)}")
            return self._get_mock_section_content(topic, section_title)
    
    def generate_slide_content(self, topic: str, section_title: str, slide_title: str, slide_type: str) -> Dict[str, Any]:
        """
        生成幻灯片内容
        
        Args:
            topic: 文档主题
            section_title: 章节标题
            slide_title: 幻灯片标题
            slide_type: 幻灯片类型 (content, two_column, image_content)
            
        Returns:
            幻灯片内容
        """
        try:
            logger.info(f"开始为幻灯片 '{slide_title}' 生成内容 (章节: {section_title}, 类型: {slide_type})")
            
            # 构建提示
            prompt = self._build_slide_prompt(topic, section_title, slide_title, slide_type)
            
            # 调用AI客户端
            messages = [
                {"role": "system", "content": "你是一个专业的PPT内容生成助手，擅长创建简洁、有力的幻灯片内容。"},
                {"role": "user", "content": prompt}
            ]
            
            response = self.ai_client.call_api(messages)
            
            if not response:
                logger.warning(f"生成幻灯片 '{slide_title}' 内容失败，使用模拟内容")
                return self._get_mock_slide_content(slide_title, slide_type)
            
            # 提取内容
            content = self.ai_client.extract_response_content(response)
            
            if not content:
                logger.warning(f"从响应中提取幻灯片 '{slide_title}' 内容失败，使用模拟内容")
                return self._get_mock_slide_content(slide_title, slide_type)
            
            # 解析内容
            slide_content = self._parse_slide_content(content, slide_title, slide_type)
            
            # 记录生成的内容摘要
            if slide_type == "content":
                points = slide_content.get("points", [])
                logger.info(f"成功生成幻灯片 '{slide_title}' 内容: {len(points)} 个要点")
                for i, point in enumerate(points[:2]):  # 只记录前2个要点
                    logger.info(f"  要点 {i+1}: {point.get('main', '未知')}")
                if len(points) > 2:
                    logger.info(f"  ... 还有 {len(points) - 2} 个要点")
            elif slide_type == "two_column":
                left_points = slide_content.get("left_points", [])
                right_points = slide_content.get("right_points", [])
                logger.info(f"成功生成幻灯片 '{slide_title}' 内容: 左侧 {len(left_points)} 个要点, 右侧 {len(right_points)} 个要点")
            elif slide_type == "image_content":
                points = slide_content.get("points", [])
                image_desc = slide_content.get("image_description", "")
                logger.info(f"成功生成幻灯片 '{slide_title}' 内容: {len(points)} 个要点, 图片描述: {image_desc[:50]}...")
            
            return slide_content
            
        except Exception as e:
            logger.error(f"生成幻灯片内容时出错: {str(e)}")
            return self._get_mock_slide_content(slide_title, slide_type)
    
    def _build_section_prompt(self, topic: str, section_title: str, doc_type: str) -> str:
        """
        构建生成章节内容的提示
        
        Args:
            topic: 文档主题
            section_title: 章节标题
            doc_type: 文档类型
            
        Returns:
            提示文本
        """
        if doc_type == "ppt":
            return f"""
            请为主题"{topic}"中的章节"{section_title}"生成详细的内容。
            
            要求:
            1. 内容应该全面、准确、专业
            2. 包含该章节的关键概念、原理和应用
            3. 使用清晰的结构和逻辑
            4. 适合PPT演示的简洁表达
            5. 内容长度适中，约500-800字
            
            请直接返回内容，不需要额外的格式或标记。
            """
        else:
            return f"""
            请为主题"{topic}"中的章节"{section_title}"生成详细的内容。
            
            要求:
            1. 内容应该全面、准确、专业
            2. 包含该章节的关键概念、原理和应用
            3. 使用清晰的结构和逻辑
            4. 适合学术或专业文档的正式表达
            5. 内容长度适中，约1000-1500字
            
            请直接返回内容，不需要额外的格式或标记。
            """
    
    def _build_slide_prompt(self, topic: str, section_title: str, slide_title: str, slide_type: str) -> str:
        """
        构建生成幻灯片内容的提示
        
        Args:
            topic: 文档主题
            section_title: 章节标题
            slide_title: 幻灯片标题
            slide_type: 幻灯片类型
            
        Returns:
            提示文本
        """
        base_prompt = f"""
        请为主题"{topic}"中章节"{section_title}"的幻灯片"{slide_title}"生成内容。
        
        幻灯片类型: {slide_type}
        """
        
        if slide_type == "content":
            return base_prompt + """
            要求:
            1. 创建3-5个简洁的要点
            2. 每个要点包含一个主要观点和1-2个支持细节
            3. 内容应该简洁明了，适合PPT展示
            
            请以JSON格式返回，格式如下:
            {
                "points": [
                    {
                        "main": "主要要点1",
                        "details": ["细节1", "细节2"]
                    },
                    ...
                ]
            }
            """
        elif slide_type == "two_column":
            return base_prompt + """
            要求:
            1. 创建左右两列内容
            2. 每列包含2-3个要点
            3. 每个要点包含一个主要观点和1-2个支持细节
            
            请以JSON格式返回，格式如下:
            {
                "left_points": [
                    {
                        "main": "左侧要点1",
                        "details": ["细节1", "细节2"]
                    },
                    ...
                ],
                "right_points": [
                    {
                        "main": "右侧要点1",
                        "details": ["细节1", "细节2"]
                    },
                    ...
                ]
            }
            """
        else:  # image_content
            return base_prompt + """
            要求:
            1. 创建3-4个要点，描述与图片相关的内容
            2. 每个要点包含一个主要观点和1-2个支持细节
            3. 添加一个图片描述，说明应该使用什么样的图片
            
            请以JSON格式返回，格式如下:
            {
                "points": [
                    {
                        "main": "主要要点1",
                        "details": ["细节1", "细节2"]
                    },
                    ...
                ],
                "image_description": "图片应该展示..."
            }
            """
    
    def _parse_slide_content(self, content: str, slide_title: str, slide_type: str) -> Dict[str, Any]:
        """
        解析幻灯片内容
        
        Args:
            content: 生成的内容
            slide_title: 幻灯片标题
            slide_type: 幻灯片类型
            
        Returns:
            解析后的幻灯片内容
        """
        try:
            import json
            import re
            
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    slide_content = json.loads(json_match.group(0))
                    
                    # 验证内容格式
                    if slide_type == "content" and "points" in slide_content:
                        return slide_content
                    elif slide_type == "two_column" and "left_points" in slide_content and "right_points" in slide_content:
                        return slide_content
                    elif slide_type == "image_content" and "points" in slide_content:
                        if "image_description" not in slide_content:
                            slide_content["image_description"] = f"关于{slide_title}的图示"
                        return slide_content
                except json.JSONDecodeError:
                    pass
            
            # 如果JSON解析失败，尝试从文本中提取内容
            if slide_type == "content":
                points = self._extract_points_from_text(content)
                return {"points": points}
            elif slide_type == "two_column":
                # 尝试分割内容为左右两部分
                parts = content.split("右侧", 1)
                if len(parts) == 2:
                    left_points = self._extract_points_from_text(parts[0])
                    right_points = self._extract_points_from_text("右侧" + parts[1])
                else:
                    # 如果无法分割，则平均分配要点
                    all_points = self._extract_points_from_text(content)
                    mid = len(all_points) // 2
                    left_points = all_points[:mid]
                    right_points = all_points[mid:]
                
                return {
                    "left_points": left_points,
                    "right_points": right_points
                }
            else:  # image_content
                points = self._extract_points_from_text(content)
                
                # 尝试提取图片描述
                image_desc = ""
                for line in content.split('\n'):
                    if "图片" in line and ("描述" in line or "说明" in line):
                        image_desc = line.split(":", 1)[-1].strip()
                        break
                
                if not image_desc:
                    image_desc = f"关于{slide_title}的图示"
                
                return {
                    "points": points,
                    "image_description": image_desc
                }
                
        except Exception as e:
            logger.error(f"解析幻灯片内容时出错: {str(e)}")
            return self._get_mock_slide_content(slide_title, slide_type)
    
    def _extract_points_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        从文本中提取要点
        
        Args:
            text: 文本内容
            
        Returns:
            要点列表
        """
        points = []
        current_main = None
        current_details = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是主要要点（通常以数字、项目符号或关键词开头）
            if re.match(r'^(\d+\.|\-|\*|\•|\○|\◆|要点|关键点|主要|首先|其次|再次|最后)', line):
                # 如果已有要点，保存它
                if current_main:
                    points.append({
                        "main": current_main,
                        "details": current_details
                    })
                
                # 开始新的要点
                current_main = re.sub(r'^(\d+\.|\-|\*|\•|\○|\◆|要点|关键点|主要|首先|其次|再次|最后)\s*', '', line)
                current_details = []
            elif current_main and line.startswith(('  ', '\t')):
                # 这是一个细节（缩进的行）
                current_details.append(line.strip())
            elif current_main:
                # 如果不是明显的细节但已有主要要点，也视为细节
                current_details.append(line)
        
        # 添加最后一个要点
        if current_main:
            points.append({
                "main": current_main,
                "details": current_details
            })
        
        # 如果没有提取到要点，创建一个默认要点
        if not points:
            points = [{"main": "重要信息", "details": [text[:100] + "..."]}]
        
        return points
    
    def _get_mock_section_content(self, topic: str, section_title: str) -> str:
        """
        获取模拟的章节内容
        
        Args:
            topic: 文档主题
            section_title: 章节标题
            
        Returns:
            模拟的章节内容
        """
        return f"""
{section_title}是{topic}的重要组成部分。本章节将详细介绍其关键概念、应用场景和发展趋势。

首先，{section_title}的基本概念建立在多年的研究和实践基础上。它包含多个核心要素，这些要素相互关联，共同构成了完整的理论体系。理解这些基本概念对于掌握整个主题至关重要。

其次，{section_title}在多个领域有广泛的应用场景。无论是在教育、商业还是技术创新方面，都能找到其成功应用的案例。这些应用不仅验证了理论的有效性，也为未来的发展提供了宝贵的经验。

最后，随着新技术和新方法的出现，{section_title}正在不断发展。未来研究将进一步探索其潜力和应用前景，我们有理由相信，它将在{topic}的发展中发挥更加重要的作用。
        """
    
    def _get_mock_slide_content(self, slide_title: str, slide_type: str) -> Dict[str, Any]:
        """
        获取模拟的幻灯片内容
        
        Args:
            slide_title: 幻灯片标题
            slide_type: 幻灯片类型
            
        Returns:
            模拟的幻灯片内容
        """
        if slide_type == "content":
            return {
                "points": [
                    {
                        "main": f"{slide_title}的核心要素",
                        "details": ["包含多个关键组成部分", "这些组成部分相互关联"]
                    },
                    {
                        "main": "应用场景广泛",
                        "details": ["适用于多个领域", "有丰富的实践案例"]
                    },
                    {
                        "main": "未来发展趋势",
                        "details": ["将继续创新和完善", "有望解决更多实际问题"]
                    }
                ]
            }
        elif slide_type == "two_column":
            return {
                "left_points": [
                    {
                        "main": "理论基础",
                        "details": ["建立在坚实的研究基础上", "有完整的理论体系"]
                    },
                    {
                        "main": "核心优势",
                        "details": ["高效、可靠", "易于实施和推广"]
                    }
                ],
                "right_points": [
                    {
                        "main": "实际应用",
                        "details": ["已在多个领域成功应用", "取得了显著成效"]
                    },
                    {
                        "main": "未来展望",
                        "details": ["将继续发展和完善", "有更广阔的应用前景"]
                    }
                ]
            }
        else:  # image_content
            return {
                "points": [
                    {
                        "main": f"{slide_title}的图示说明",
                        "details": ["直观展示关键概念", "帮助理解复杂关系"]
                    },
                    {
                        "main": "实际案例",
                        "details": ["展示真实应用场景", "验证理论的有效性"]
                    },
                    {
                        "main": "对比分析",
                        "details": ["与其他方法的对比", "突出独特优势"]
                    }
                ],
                "image_description": f"关于{slide_title}的图示，展示其核心概念和关系"
            } 