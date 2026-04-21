#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧本结构化解析器 (Pipeline Parser)
将原始剧本文本解析为结构化 JSON 数据，供后续步骤（情绪节拍拆解、镜头切分、提示词撰写）使用。

输入：剧本原文（字符串）
输出：结构化 JSON（字典）

设计原则：
- 一次性提取基础信息（角色、场景、台词），避免后续步骤重复读取原文
- 保持轻量，复杂分析（情绪判断、导演决策）仍由 AI 完成
- 输出格式与 SKILL.md Step 2.5 定义一致
"""

import re
import json
from typing import List, Dict, Tuple, Optional

class ScriptParser:
    def __init__(self):
        # 场景正则：[场景：...] 或 场景：... 或 数字-数字开头（如 03-1苏府，夜，内）
        self.scene_pattern = re.compile(
            r'^\s*\[?\s*场景\s*[:：]\s*(.+?)\s*\]?$|'  # 标准场景标记
            r'^\s*\d+-\d+\s*(.+?)$'  # 数字-数字开头（如 03-1苏府，夜，内）
        )
        # 台词正则：角色名（情绪）: 台词 或 角色名: 台词
        # 支持中文括号（）和英文括号()
        self.dialogue_pattern = re.compile(
            r'^\s*([\u4e00-\u9fffA-Za-z0-9_]+)\s*[（(]([^）)]+)[）)]\s*[:：]\s*(.+)$|'  # 带情绪
            r'^\s*([\u4e00-\u9fffA-Za-z0-9_]+)\s*[:：]\s*(.+)$'  # 不带情绪
        )
        # 动作描述正则：（动作）或 [动作] 或纯描述
        self.action_pattern = re.compile(r'^\s*[（\[].*[）\]]\s*$')
        
    def parse(self, script_text: str) -> Dict:
        """解析剧本文本，返回结构化数据"""
        lines = script_text.strip().split('\n')
        
        # 初始化数据结构
        characters = {}
        scenes = {}
        dialogues = []
        current_scene = None
        current_scene_has_ref = False  # 默认无参考图，后续由用户确认
        
        for line_num, line in enumerate(lines):
            line = line.rstrip()
            if not line:
                continue
                
            # 1. 检查是否为场景行
            scene_match = self.scene_pattern.match(line)
            if scene_match:
                # 新正则有两个捕获组：group1（标准场景），group2（数字格式）
                scene_name = scene_match.group(1) if scene_match.group(1) else scene_match.group(2)
                if scene_name:
                    scene_name = scene_name.strip()
                    # 移除控制字符（如\x01）
                    scene_name = re.sub(r'[\x00-\x1F\x7F]', '', scene_name)
                    # 移除前导标点（如顿号、空格）
                    scene_name = scene_name.lstrip('、')
                    current_scene = scene_name
                    if scene_name not in scenes:
                        scenes[scene_name] = {
                            "name": scene_name,
                            "count": 0,
                            "has_ref": False  # 待确认
                        }
                    scenes[scene_name]["count"] += 1
                continue
                
            # 跳过非台词的特殊行（出字幕、人物介绍等）
            skip_keywords = ["出字幕：", "人物："]
            if any(line.startswith(keyword) for keyword in skip_keywords):
                continue
            
            # 2. 检查是否为台词行（包含角色和情绪）
            dialogue_match = self.dialogue_pattern.match(line)
            if dialogue_match:
                # 检查带情绪的模式（group1, group2, group3）
                if dialogue_match.group(1):
                    char_name = dialogue_match.group(1).strip()
                    emotion = dialogue_match.group(2).strip() if dialogue_match.group(2) else None
                    content = dialogue_match.group(3).strip()
                else:
                    # 不带情绪的模式（group4, group5）
                    char_name = dialogue_match.group(4).strip()
                    emotion = None
                    content = dialogue_match.group(5).strip()
                
                # 统计角色出现次数
                if char_name not in characters:
                    characters[char_name] = {
                        "name": char_name,
                        "count": 0
                    }
                characters[char_name]["count"] += 1
                
                # 判断台词类型和计算时长
                speed_type, duration = self.estimate_dialogue_duration(content, emotion)
                
                dialogues.append({
                    "content": content,
                    "character": char_name,
                    "emotion": emotion,
                    "emotional_direction": emotion,  # 兼容SKILL.md字段名
                    "speed_type": speed_type,
                    "duration": duration,
                    "scene": current_scene,
                    "line_num": line_num
                })
                continue
                
            # 3. 检查是否为动作描述行（方括号或圆括号内的文本）
            if self.action_pattern.match(line):
                # 动作描述暂不单独存储，将在情绪节拍拆解中处理
                continue
                
            # 4. 其他文本（如旁白、环境描述等）暂不解析，由AI处理
            continue
        
        # 转换为列表格式
        character_list = [{"name": name, "count": data["count"]} 
                         for name, data in characters.items()]
        
        scene_list = [{"name": name, "count": data["count"], "has_ref": data["has_ref"]}
                     for name, data in scenes.items()]
        
        # 根据出现次数标记参考图（重复3次以上默认有参考图）
        for char in character_list:
            char["has_ref_default"] = char["count"] >= 3
        for scene in scene_list:
            scene["has_ref_default"] = scene["count"] >= 3
        
        return {
            "characters": character_list,
            "scenes": scene_list,
            "dialogues": dialogues,
            "emotional_beats": [],  # 由后续AI分析填充
            "director_decisions": {
                "narrative_order": [],
                "space_scheduling": {},
                "omissions": []
            },
            "metadata": {
                "total_lines": len(lines),
                "total_dialogues": len(dialogues),
                "total_characters": len(characters),
                "total_scenes": len(scenes)
            }
        }
    
    def estimate_dialogue_duration(self, content: str, emotion: Optional[str]) -> Tuple[str, float]:
        """
        估算台词时长
        返回: (speed_type, duration_in_seconds)
        """
        # 计算字数（中文字符和标点）
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
        punctuation = re.findall(r'[，。！？；：、]', content)
        word_count = len(chinese_chars) + len(punctuation) * 0.5  # 标点折半
        
        # 根据情绪和内容判断语速类型
        speed_type = "normal"
        if emotion:
            emotion_lower = emotion.lower()
            if any(keyword in emotion_lower for keyword in ["急促", "高声", "怒吼", "大喊", "尖叫"]):
                speed_type = "fast"
            elif any(keyword in emotion_lower for keyword in ["内心", "低语", "轻声", "自语"]):
                speed_type = "os"
            elif any(keyword in emotion_lower for keyword in ["沉重", "缓慢", "低沉"]):
                speed_type = "slow"
        
        # 语速基准（字/秒）
        speed_map = {
            "fast": 5.5,    # 5-6字/秒
            "normal": 4.5,  # 4-5字/秒
            "os": 3.5,      # 3-4字/秒
            "slow": 3.0     # 2.5-3.5字/秒
        }
        
        base_speed = speed_map.get(speed_type, 4.5)
        
        # 基本时长 = 字数 / 语速
        base_duration = word_count / base_speed if word_count > 0 else 0
        
        # 添加停顿（句号、问号、叹号）
        sentence_ends = len(re.findall(r'[。！？]', content))
        comma_ends = len(re.findall(r'[，；]', content))
        
        # 停顿规则：句号1秒，逗号0.5秒
        pause_duration = sentence_ends * 1.0 + comma_ends * 0.5
        
        # 急促台词停顿较短
        if speed_type == "fast":
            pause_duration *= 0.6
        
        total_duration = base_duration + pause_duration
        
        # 最小时长保护
        if total_duration < 1.5:
            total_duration = 1.5
            
        return speed_type, round(total_duration)
    
    def to_json(self, data: Dict, indent: int = 2) -> str:
        """将结构化数据转为JSON字符串"""
        return json.dumps(data, ensure_ascii=False, indent=indent)


def main():
    """命令行接口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python parser.py <剧本文件路径>")
        print("或: python parser.py --stdin (从标准输入读取)")
        sys.exit(1)
    
    parser = ScriptParser()
    
    if sys.argv[1] == "--stdin":
        # 从标准输入读取
        script_text = sys.stdin.read()
    else:
        # 从文件读取
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            script_text = f.read()
    
    # 解析
    structured_data = parser.parse(script_text)
    
    # 输出JSON
    json_output = parser.to_json(structured_data)
    print(json_output)


if __name__ == "__main__":
    main()