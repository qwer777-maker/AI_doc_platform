import os
import json
import requests
from typing import List, Dict, Any, Optional
import logging
from ..core.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekService:
    def __init__(self):
        self.api_key = os.getenv("AI_API_KEY", "")
        self.api_endpoint = os.getenv("AI_API_ENDPOINT", "https://api.deepseek.com/v1/chat/completions")
        
        if not self.api_key:
            logger.error("DeepSeek API密钥未设置")
            raise ValueError("DeepSeek API密钥未设置")
        
        logger.info(f"DeepSeek服务初始化完成，API端点: {self.api_endpoint}")
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def generate_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        使用DeepSeek API生成文本完成
        
        Args:
            messages: 消息列表，格式为[{"role": "user", "content": "你好"}]
            temperature: 温度参数，控制随机性
            max_tokens: 生成的最大token数
            
        Returns:
            生成的文本，如果请求失败则返回None
        """
        try:
            payload = {
                "model": "deepseek-chat",  # 或其他可用模型
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"API请求失败: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"调用DeepSeek API时出错: {str(e)}")
            return None
    
    def generate_document_outline(self, topic: str, doc_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        生成文档大纲
        """
        try:
            # 1. 首先生成主要章节
            main_sections = self._generate_main_sections(topic, doc_type)
            if not main_sections:
                return None
            
            # 2. 然后为每个章节生成子章节
            outline = []
            for section in main_sections:
                section_detail = self._generate_section_detail(topic, section, doc_type)
                if section_detail:
                    outline.append(section_detail)
            
            return outline
            
        except Exception as e:
            logger.error(f"生成大纲时出错: {str(e)}")
            return None
    
    def generate_section_content(self, topic: str, section_title: str, doc_type: str) -> str:
        """
        生成文档章节内容
        """
        try:
            logger.info(f"为章节 '{section_title}' 生成内容")
            
            # 如果没有 API 密钥，使用模拟数据
            if not self.api_key:
                return self._get_mock_section_content(topic, section_title)
            
            # 构建提示
            prompt = self._build_section_prompt(topic, section_title, doc_type)
            
            # 调用 API
            response = self._call_api(prompt)
            
            if not response:
                return self._get_mock_section_content(topic, section_title)
            
            # 提取内容
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                return self._get_mock_section_content(topic, section_title)
            
            return content
            
        except Exception as e:
            logger.error(f"生成章节内容时出错: {str(e)}")
            return self._get_mock_section_content(topic, section_title)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _call_api(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        调用 DeepSeek API
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是一个专业的文档生成助手，擅长创建结构化的文档大纲和内容。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            # 增加超时时间到120秒
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=data,
                timeout=120  # 增加到120秒
            )
            
            # 添加更详细的日志
            logger.info(f"API响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"API请求失败: {response.status_code} - {response.text}")
                return None
            
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error("API请求超时，可能需要更长的处理时间")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求异常: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"API调用出错: {str(e)}")
            return None
    
    def _build_outline_prompt(self, topic: str, doc_type: str) -> str:
        """
        构建大纲生成提示
        """
        if doc_type == "ppt":
            return f"""
            请为主题"{topic}"创建一个详细的PPT演示文稿大纲。
            
            要求:
            1. 包含一个引人入胜的标题幻灯片
            2. 包含目录幻灯片
            3. 创建5-7个主要章节
            4. 每个章节下包含2-4个子幻灯片
            5. 包含一个总结幻灯片
            
            请以JSON格式返回，格式如下:
            {{
                "title": "演示文稿标题",
                "sections": [
                    {{
                        "title": "章节1标题",
                        "slides": [
                            {{
                                "title": "幻灯片1标题",
                                "type": "content"
                            }},
                            ...
                        ]
                    }},
                    ...
                ]
            }}
            
            确保JSON格式正确，可以直接解析。
            """
        elif doc_type == "word":
            return f"""
            请为主题"{topic}"创建一个详细的Word文档大纲。
            
            要求:
            1. 包含一个引人入胜的标题
            2. 包含摘要部分
            3. 创建5-7个主要章节
            4. 每个章节下包含2-4个子章节
            5. 包含结论部分
            6. 包含参考文献部分
            
            请以JSON格式返回，格式如下:
            {{
                "title": "文档标题",
                "sections": [
                    {{
                        "title": "章节1标题",
                        "subsections": [
                            {{
                                "title": "子章节1标题"
                            }},
                            ...
                        ]
                    }},
                    ...
                ]
            }}
            
            确保JSON格式正确，可以直接解析。
            """
        else:
            return f"""
            请为主题"{topic}"创建一个详细的文档大纲。
            
            要求:
            1. 包含一个引人入胜的标题
            2. 创建5-7个主要章节
            3. 每个章节下包含2-4个子章节
            4. 包含结论部分
            
            请以JSON格式返回，格式如下:
            {{
                "title": "文档标题",
                "sections": [
                    {{
                        "title": "章节1标题",
                        "subsections": [
                            {{
                                "title": "子章节1标题"
                            }},
                            ...
                        ]
                    }},
                    ...
                ]
            }}
            
            确保JSON格式正确，可以直接解析。
            """
    
    def _build_section_prompt(self, topic: str, section_title: str, doc_type: str) -> str:
        """
        构建章节内容生成提示
        """
        if doc_type == "ppt":
            return f"""
            请为主题"{topic}"的PPT演示文稿中的"{section_title}"章节生成内容。
            
            要求:
            1. 内容应该简洁明了，适合PPT展示
            2. 包含3-5个要点
            3. 每个要点不超过2-3句话
            4. 可以包含一些建议的图表或图像描述
            
            请直接返回内容，不需要额外的格式。
            """
        else:
            return f"""
            请为主题"{topic}"的文档中的"{section_title}"章节生成详细内容。
            
            要求:
            1. 内容应该详细且信息丰富
            2. 包含相关的事实、数据或例子
            3. 内容长度应该在300-500字之间
            4. 语言应该专业且易于理解
            
            请直接返回内容，不需要额外的格式。
            """
    
    def _parse_outline_response(self, response: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        解析API响应，提取大纲
        """
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                return None
            
            # 尝试从内容中提取JSON
            # 首先尝试直接解析
            try:
                outline_data = json.loads(content)
                return outline_data.get("sections", [])
            except json.JSONDecodeError:
                pass
            
            # 如果直接解析失败，尝试从文本中提取JSON部分
            try:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    outline_data = json.loads(json_str)
                    return outline_data.get("sections", [])
            except (json.JSONDecodeError, ValueError):
                pass
            
            # 如果仍然失败，尝试更宽松的解析方法
            logger.warning("无法解析JSON响应，尝试手动解析")
            
            # 简单的章节提取
            sections = []
            lines = content.split("\n")
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 检查是否是章节标题
                if line.startswith("#") or line.startswith("章节") or line.startswith("Section"):
                    title = line.lstrip("#").strip()
                    if ":" in title:
                        title = title.split(":", 1)[1].strip()
                    
                    current_section = {"title": title, "subsections": []}
                    sections.append(current_section)
                
                # 检查是否是子章节
                elif current_section and (line.startswith("-") or line.startswith("*")):
                    title = line.lstrip("-*").strip()
                    if ":" in title:
                        title = title.split(":", 1)[1].strip()
                    
                    current_section["subsections"].append({"title": title})
            
            if sections:
                return sections
            
            # 如果所有方法都失败，返回None
            return None
            
        except Exception as e:
            logger.error(f"解析大纲响应时出错: {str(e)}")
            return None
    
    def _get_mock_outline(self, topic: str, doc_type: str) -> List[Dict[str, Any]]:
        """
        生成模拟大纲数据
        """
        if doc_type == "ppt":
            return [
                {
                    "title": f"介绍 {topic}",
                    "slides": [
                        {"title": "什么是" + topic, "type": "content"},
                        {"title": topic + "的重要性", "type": "content"},
                        {"title": "本演示文稿概述", "type": "content"}
                    ]
                },
                {
                    "title": f"{topic} 的历史",
                    "slides": [
                        {"title": "早期发展", "type": "content"},
                        {"title": "关键里程碑", "type": "content"},
                        {"title": "现代进展", "type": "content"}
                    ]
                },
                {
                    "title": f"{topic} 的主要特点",
                    "slides": [
                        {"title": "核心特性", "type": "content"},
                        {"title": "优势分析", "type": "content"},
                        {"title": "潜在挑战", "type": "content"}
                    ]
                },
                {
                    "title": f"{topic} 的应用",
                    "slides": [
                        {"title": "行业应用", "type": "content"},
                        {"title": "实际案例", "type": "content"},
                        {"title": "成功故事", "type": "content"}
                    ]
                },
                {
                    "title": f"{topic} 的未来",
                    "slides": [
                        {"title": "发展趋势", "type": "content"},
                        {"title": "未来机遇", "type": "content"},
                        {"title": "预测与展望", "type": "content"}
                    ]
                },
                {
                    "title": "总结与问答",
                    "slides": [
                        {"title": "关键要点回顾", "type": "content"},
                        {"title": "结论", "type": "content"},
                        {"title": "问答环节", "type": "content"}
                    ]
                }
            ]
        else:
            return [
                {
                    "title": f"引言",
                    "subsections": [
                        {"title": "研究背景"},
                        {"title": "研究目的"},
                        {"title": "研究意义"}
                    ]
                },
                {
                    "title": f"{topic} 概述",
                    "subsections": [
                        {"title": "定义与概念"},
                        {"title": "历史发展"},
                        {"title": "理论基础"}
                    ]
                },
                {
                    "title": f"{topic} 的主要特点",
                    "subsections": [
                        {"title": "核心特性"},
                        {"title": "技术原理"},
                        {"title": "关键要素"}
                    ]
                },
                {
                    "title": f"{topic} 的应用领域",
                    "subsections": [
                        {"title": "行业应用"},
                        {"title": "典型案例"},
                        {"title": "应用效果"}
                    ]
                },
                {
                    "title": f"{topic} 的挑战与机遇",
                    "subsections": [
                        {"title": "当前挑战"},
                        {"title": "发展机遇"},
                        {"title": "解决方案"}
                    ]
                },
                {
                    "title": "结论与展望",
                    "subsections": [
                        {"title": "研究结论"},
                        {"title": "未来展望"},
                        {"title": "建议"}
                    ]
                },
                {
                    "title": "参考文献",
                    "subsections": []
                }
            ]
    
    def _get_mock_section_content(self, topic: str, section_title: str) -> str:
        """
        生成模拟章节内容
        """
        return f"""
        这是关于"{topic}"主题下"{section_title}"章节的内容。
        
        {section_title}是{topic}的重要组成部分。它涉及多个关键方面，包括基本原理、应用场景和发展趋势。
        
        首先，{section_title}的基本原理建立在多年的研究和实践基础上。研究表明，理解这些原理对于掌握{topic}至关重要。
        
        其次，{section_title}在多个领域有广泛应用。例如，在教育、商业和技术创新方面都发挥着重要作用。
        
        最后，{section_title}正在不断发展。随着新技术和新方法的出现，我们可以预见它在未来将有更多创新和突破。
        
        总之，{section_title}是理解和应用{topic}的关键环节，值得我们深入研究和探索。
        """

    def _generate_main_sections(self, topic: str, doc_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        生成文档的主要章节
        """
        try:
            logger.info(f"为主题 '{topic}' 生成主要章节")
            
            # 构建提示
            prompt = self._build_main_sections_prompt(topic, doc_type)
            
            # 调用 API
            response = self._call_api(prompt)
            
            if not response:
                logger.error("生成主要章节失败")
                return None
            
            # 打印原始响应以便调试
            logger.info(f"API原始响应: {response}")
            
            # 解析响应
            try:
                content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
                logger.info(f"解析前的内容: {content}")
                
                # 尝试清理和格式化内容
                content = content.strip()
                if not content.startswith("{"):
                    # 如果返回的不是JSON格式，尝试提取JSON部分
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        content = json_match.group()
                    else:
                        # 如果无法提取JSON，构造一个基本的章节结构
                        sections = self._extract_sections_from_text(content)
                        return sections
                
                sections = json.loads(content)
                return sections.get("sections", [])
            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                logger.error(f"解析主要章节响应失败: {str(e)}")
                # 如果JSON解析失败，尝试从文本中提取章节
                return self._extract_sections_from_text(content)
            
        except Exception as e:
            logger.error(f"生成主要章节时出错: {str(e)}")
            return None

    def _extract_sections_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取章节结构
        """
        try:
            # 移除可能的代码块标记
            text = text.replace("```json", "").replace("```", "")
            
            # 尝试找出章节标题
            sections = []
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # 跳过空行
                if not line:
                    continue
                # 跳过常见的无关文本
                if any(skip in line.lower() for skip in ['要求:', '格式:', 'json', '章节']):
                    continue
                # 提取可能的章节标题
                if ':' in line:
                    title = line.split(':')[1].strip()
                else:
                    title = line.strip('"').strip()
                
                if title and len(title) < 100:  # 避免提取过长的文本作为标题
                    sections.append({"title": title})
            
            # 如果没有找到任何章节，创建默认章节
            if not sections:
                sections = [
                    {"title": "引言"},
                    {"title": "主要内容"},
                    {"title": "结论"}
                ]
            
            return sections
        except Exception as e:
            logger.error(f"从文本提取章节失败: {str(e)}")
            # 返回默认章节结构
            return [
                {"title": "引言"},
                {"title": "主要内容"},
                {"title": "结论"}
            ]

    def _build_main_sections_prompt(self, topic: str, doc_type: str) -> str:
        """
        构建生成主要章节的提示
        """
        if doc_type == "ppt":
            return f"""
            请为主题"{topic}"创建PPT演示文稿的主要章节结构。
            
            要求:
            1. 创建5-7个主要章节
            2. 每个章节应该简洁明了
            3. 章节之间应该有逻辑连贯性
            4. 严格按照以下JSON格式返回，不要添加其他说明文字：
            
            {{
                "sections": [
                    {{
                        "title": "引言"
                    }},
                    {{
                        "title": "第二章节标题"
                    }},
                    ...
                ]
            }}
            """
        else:
            return f"""
            请为主题"{topic}"创建Word文档的主要章节结构。
            
            要求:
            1. 创建5-7个主要章节
            2. 包含引言和结论章节
            3. 章节之间应该有逻辑连贯性
            4. 严格按照以下JSON格式返回，不要添加其他说明文字：
            
            {{
                "sections": [
                    {{
                        "title": "引言"
                    }},
                    {{
                        "title": "第二章节标题"
                    }},
                    ...
                ]
            }}
            """

    def _generate_section_detail(self, topic: str, section: Dict[str, Any], doc_type: str) -> Optional[Dict[str, Any]]:
        """
        为每个主要章节生成详细内容
        """
        try:
            section_title = section.get("title", "")
            logger.info(f"为章节 '{section_title}' 生成详细内容")
            
            # 构建提示
            prompt = self._build_section_detail_prompt(topic, section_title, doc_type)
            
            # 调用 API
            response = self._call_api(prompt)
            
            if not response:
                logger.error(f"生成章节 '{section_title}' 的详细内容失败")
                return None
            
            # 打印原始响应以便调试
            logger.info(f"章节详细内容API响应: {response}")
            
            # 解析响应
            try:
                content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
                logger.info(f"章节详细内容解析前的内容: {content}")
                
                # 尝试清理和格式化内容
                content = content.strip()
                if not content.startswith("{"):
                    # 如果返回的不是JSON格式，尝试提取JSON部分
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        content = json_match.group()
                    else:
                        # 如果无法提取JSON，构造一个基本的子章节结构
                        subsections = self._extract_subsections_from_text(content, section_title)
                        return {
                            "title": section_title,
                            "slides" if doc_type == "ppt" else "subsections": subsections
                        }
                
                detail = json.loads(content)
                return {
                    "title": section_title,
                    "slides" if doc_type == "ppt" else "subsections": detail.get("content", [])
                }
            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                logger.error(f"解析章节详细内容失败: {str(e)}")
                # 如果JSON解析失败，尝试从文本中提取子章节
                subsections = self._extract_subsections_from_text(content, section_title)
                return {
                    "title": section_title,
                    "slides" if doc_type == "ppt" else "subsections": subsections
                }
            
        except Exception as e:
            logger.error(f"生成章节详细内容时出错: {str(e)}")
            return None

    def _extract_subsections_from_text(self, text: str, section_title: str) -> List[Dict[str, Any]]:
        """
        从文本中提取子章节结构，增加对PPT内容的支持
        """
        try:
            # 移除可能的代码块标记
            text = text.replace("```json", "").replace("```", "")
            
            # 尝试找出幻灯片内容
            subsections = []
            current_slide = None
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 跳过常见的无关文本
                if any(skip in line.lower() for skip in ['要求:', '格式:', 'json', '内容:']):
                    continue
                
                # 检测新的幻灯片标题
                if line.endswith('：') or line.endswith(':') or line.startswith('#'):
                    if current_slide:
                        subsections.append(current_slide)
                    current_slide = {
                        "title": line.rstrip('：:').lstrip('#').strip(),
                        "type": "content",
                        "points": [],
                        "notes": ""
                    }
                # 收集要点
                elif current_slide and (line.startswith('-') or line.startswith('•')):
                    point = line.lstrip('-•').strip()
                    if len(point) > 40:  # 限制要点字数
                        point = point[:37] + '...'
                    current_slide["points"].append(point)
                    
                    # 限制每页幻灯片的要点数量
                    if len(current_slide["points"]) > 5:
                        current_slide["points"] = current_slide["points"][:5]
                
                # 收集补充说明
                elif current_slide and line.startswith('注：'):
                    notes = line.lstrip('注：').strip()
                    if len(notes) > 100:  # 限制注释字数
                        notes = notes[:97] + '...'
                    current_slide["notes"] = notes
            
            # 添加最后一个幻灯片
            if current_slide:
                subsections.append(current_slide)
            
            # 如果没有找到任何内容，创建默认内容
            if not subsections:
                subsections = [
                    {
                        "title": f"{section_title[:15]}概述",
                        "type": "content",
                        "points": [
                            f"介绍{section_title[:15]}的定义和范围",
                            f"分析{section_title[:15]}的重要性",
                            f"探讨主要应用场景"
                        ],
                        "notes": f"本节重点讲解{section_title[:15]}的核心内容，帮助听众理解基本概念和重要性。"
                    },
                    {
                        "title": "核心要点",
                        "type": "content",
                        "points": [
                            "关键要点1（具体相关内容）",
                            "关键要点2（具体相关内容）",
                            "关键要点3（具体相关内容）"
                        ],
                        "notes": "详细展开各个要点，突出重要性和应用价值。"
                    },
                    {
                        "title": "总结与展望",
                        "type": "content",
                        "points": [
                            "回顾核心观点",
                            "强调实践意义",
                            "展望未来方向"
                        ],
                        "notes": "总结本节重点，强调实践价值，为下一节内容做铺垫。"
                    }
                ]
            
            return subsections
        except Exception as e:
            logger.error(f"从文本提取子章节失败: {str(e)}")
            # 返回默认结构
            return [
                {
                    "title": f"{section_title[:15]}概述",
                    "type": "content",
                    "points": [
                        f"介绍{section_title[:15]}的定义和范围",
                        f"分析{section_title[:15]}的重要性",
                        f"探讨主要应用场景"
                    ],
                    "notes": f"本节重点讲解{section_title[:15]}的核心内容，帮助听众理解基本概念和重要性。"
                }
            ]

    def _build_section_detail_prompt(self, topic: str, section_title: str, doc_type: str) -> str:
        """
        构建生成章节详细内容的提示
        """
        if doc_type == "ppt":
            return f"""
            请为主题"{topic}"的章节"{section_title}"创建详细的PPT幻灯片内容。

            要求:
            1. 创建3-4个幻灯片，可以使用以下布局类型：
               - normal: 普通内容布局
               - image_content: 带图片的布局
               - two_column: 双栏布局
            2. 内容限制：
               - 标题：20字以内
               - 主要要点：40字以内
               - 每个要点的详细说明：2-3个子要点，每个20-30字
               - 每页3-5个主要要点
               - 注释：100字以内
            3. 双栏布局时，左右两栏内容要相互呼应
            4. 严格按照以下JSON格式返回：

            {{
                "content": [
                    {{
                        "title": "幻灯片标题",
                        "type": "normal",
                        "points": [
                            {{
                                "main": "主要要点1",
                                "details": [
                                    "要点1的详细说明1",
                                    "要点1的详细说明2"
                                ]
                            }},
                            {{
                                "main": "主要要点2",
                                "details": [
                                    "要点2的详细说明1",
                                    "要点2的详细说明2"
                                ]
                            }}
                        ],
                        "notes": "演讲注释"
                    }},
                    {{
                        "title": "对比分析",
                        "type": "two_column",
                        "left_points": [
                            {{
                                "main": "左栏要点1",
                                "details": ["详细说明1", "详细说明2"]
                            }}
                        ],
                        "right_points": [
                            {{
                                "main": "右栏要点1",
                                "details": ["详细说明1", "详细说明2"]
                            }}
                        ],
                        "notes": "演讲注释"
                    }}
                ]
            }}
            """
        else:
            return f"""
            请为主题"{topic}"的章节"{section_title}"创建详细的子章节结构。
            
            要求:
            1. 创建2-4个子章节
            2. 每个子章节应该有明确的主题
            3. 内容应该详实专业
            4. 严格按照以下JSON格式返回，不要添加其他说明文字：
            
            {{
                "content": [
                    {{
                        "title": "第一个子章节标题"
                    }},
                    {{
                        "title": "第二个子章节标题"
                    }}
                ]
            }}
            """ 