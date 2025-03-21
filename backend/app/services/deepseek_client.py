import os
import logging
from typing import List, Dict, Any, Optional

from .ai_client import AIClient

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekClient(AIClient):
    """
    DeepSeek API客户端实现
    """
    
    def __init__(self, api_key: Optional[str] = None, api_endpoint: Optional[str] = None):
        """
        初始化DeepSeek客户端
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            api_endpoint: API端点，如果为None则从环境变量获取
        """
        # 如果未提供API端点，使用DeepSeek默认端点
        default_endpoint = "https://api.deepseek.com/v1/chat/completions"
        super().__init__(
            api_key=api_key, 
            api_endpoint=api_endpoint or os.getenv("AI_API_ENDPOINT", default_endpoint)
        )
        logger.info("DeepSeek客户端初始化完成")
    
    def _prepare_payload(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> Dict[str, Any]:
        """
        准备DeepSeek API请求的payload
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            准备好的payload
        """
        return {
            "model": "deepseek-chat",  # 或其他可用模型
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
    
    def extract_response_content(self, response: Dict[str, Any]) -> Optional[str]:
        """
        从DeepSeek API响应中提取内容
        
        Args:
            response: API响应
            
        Returns:
            提取的内容，如果提取失败则返回None
        """
        if not response or "choices" not in response:
            return None
        
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"从响应中提取内容时出错: {str(e)}")
            return None 