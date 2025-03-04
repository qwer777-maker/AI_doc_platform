import os
import json
import requests
from typing import List, Dict, Any, Optional
import logging
from ..core.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekService:
    def __init__(self):
        self.api_key = os.getenv("AI_API_KEY", "")
        self.api_endpoint = os.getenv("AI_API_ENDPOINT", "https://api.deepseek.com/v1/chat/completions")
        
        if not self.api_key:
            logger.warning("DeepSeek API 密钥未设置，将使用模拟数据")
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
            logger.info(f"为主题 '{topic}' 生成 {doc_type} 文档大纲")
            
            # 如果没有 API 密钥，使用模拟数据
            if not self.api_key:
                return self._get_mock_outline(topic, doc_type)
            
            # 构建提示
            prompt = self._build_outline_prompt(topic, doc_type)
            
            # 调用 API
            response = self._call_api(prompt)
            
            if not response:
                logger.error("API 调用失败")
                return self._get_mock_outline(topic, doc_type)  # 失败时使用模拟数据
            
            # 解析响应
            outline = self._parse_outline_response(response)
            
            if not outline:
                logger.error("无法解析大纲响应")
                return self._get_mock_outline(topic, doc_type)  # 解析失败时使用模拟数据
            
            return outline
            
        except Exception as e:
            logger.error(f"生成大纲时出错: {str(e)}")
            return self._get_mock_outline(topic, doc_type)  # 出错时使用模拟数据
    
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
            
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"API 请求失败: {response.status_code} - {response.text}")
                return None
            
            return response.json()
            
        except Exception as e:
            logger.error(f"API 调用出错: {str(e)}")
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