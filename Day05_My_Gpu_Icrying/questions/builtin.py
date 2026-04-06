"""
内置测试题目 - 你的20道综合能力测试题
"""

from typing import List, Optional
from .base import Question, QuestionCategory, DifficultyLevel


def get_builtin_questions() -> List[Question]:
    """获取所有内置测试题目"""
    return [
        # ========== 逻辑与推理 ==========
        Question(
            id="L001",
            category=QuestionCategory.LOGIC,
            difficulty=DifficultyLevel.HARD,
            title="序列推理",
            content="观察以下序列的规律，填写空缺项：\n2, 6, 15, 40, 104, ?\n（提示：这不是简单的数学序列）",
            answer="273",
            keywords=["273", "递推", "规律", "(a+b)*2", "(2+6)*2-1"],
            hints="观察相邻数字的关系，尝试寻找递推公式",
            score=10,
            metadata={
                "explanation": "规律：从第三项开始，每一项 = (前两项之和) × 2 + 修正项。\n"
                              "15 = (2+6)×2 - 1 = 15\n"
                              "40 = (6+15)×2 - 2 = 40\n"
                              "104 = (15+40)×2 - 6 = 104\n"
                              "273 = (40+104)×2 - 11 = 273",
                "trap": "容易误以为是乘法关系或幂次关系"
            }
        ),
        
        Question(
            id="L002",
            category=QuestionCategory.LOGIC,
            difficulty=DifficultyLevel.MEDIUM,
            title="条件逻辑陷阱",
            content="""前提：
1. 所有能飞的动物都是鸟类
2. 蝙蝠能飞
3. 企鹅是鸟类但不能飞

问题：根据以上前提，"所有鸟类都能飞"是否正确？为什么？""",
            answer="不正确。前提1只说能飞的动物是鸟类，但没说所有鸟类都能飞。前提3明确说明企鹅是鸟类但不能飞，构成反例。",
            keywords=["不正确", "反例", "企鹅", "前提1", "充分不必要"],
            score=10,
            metadata={
                "trap": "这是一个经典的逻辑逆命题错误。前提1是'能飞→鸟类'，不能推出'鸟类→能飞'",
                "logic_type": "充分必要条件陷阱"
            }
        ),
        
        Question(
            id="L003",
            category=QuestionCategory.LOGIC,
            difficulty=DifficultyLevel.EXPERT,
            title="空间拓扑推理",
            content="一个立方体有6个面，每个面被涂上不同颜色。如果将立方体切割成27个小立方体（3×3×3），然后随机重新组装成一个大立方体，有多少种可能的外观组合？（不考虑旋转对称性）",
            answer="30种",
            keywords=["30", "排列", "6!", "720", "对称性"],
            hints="考虑6个面的颜色排列，注意旋转对称性会减少不同外观的数量",
            score=15,
            metadata={
                "explanation": "6个面涂不同颜色，排列数为6! = 720。立方体有24种旋转对称（6个面×每个面4种旋转），所以不同外观 = 720/24 = 30种",
                "math": "考虑Burnside引理或直接枚举"
            }
        ),
        
        Question(
            id="L004",
            category=QuestionCategory.LOGIC,
            difficulty=DifficultyLevel.HARD,
            title="悖论识别",
            content=""""这句话是假的。"

如果你认为这句话是假的，那它就是真的；如果你认为它是真的，那它就是假的。

请分析这个陈述的逻辑结构，并说明AI应该如何处理此类自我指涉的悖论。""",
            answer="这是著名的'说谎者悖论'。AI应识别其自我指涉结构，承认这类陈述在经典二值逻辑中无法赋予真值，可采用多值逻辑或层次化语义分析。",
            keywords=["说谎者悖论", "自我指涉", "Liar Paradox", "真值", "层次化"],
            score=15,
            metadata={
                "theory": "Liar Paradox - 最简单的自我指涉悖论",
                "approach": "Tarski的元语言层次理论、Kripke的真值间隙理论、或Paraconsistent逻辑"
            }
        ),
        
        Question(
            id="L005",
            category=QuestionCategory.LOGIC,
            difficulty=DifficultyLevel.EXPERT,
            title="多约束规划",
            content="""有五座房子排成一排，颜色各不相同。五个人分别住在里面，每个人都有不同的国籍、喝不同的饮料、抽不同品牌的香烟、养不同的宠物。

已知条件（爱因斯坦谜题简化版）：
1. 英国人住红色房子
2. 瑞典人养狗
3. 丹麦人喝茶
4. 绿色房子在白色房子左边且相邻
5. 绿色房子主人喝咖啡
6. 抽Pall Mall香烟的人养鸟
7. 黄色房子主人抽Dunhill
8. 中间房子的人喝牛奶
9. 挪威人住第一间
10. 抽Blends的人住在养猫的人隔壁
11. 养马的人住在抽Dunhill的人隔壁
12. 抽Blue Master的人喝啤酒
13. 德国人抽Prince
14. 挪威人住蓝色房子隔壁
15. 抽Blends的人有一个喝水的邻居

问题：谁养鱼？""",
            answer="德国人养鱼",
            keywords=["德国人", "German", "养鱼", "绿色房子"],
            hints="使用排除法和填表法，从确定性条件开始推理",
            score=20,
            metadata={
                "type": "逻辑谜题",
                "difficulty": "高",
                "note": "这是著名的爱因斯坦谜题，完整解答需要系统性的表格推理"
            }
        ),
        
        # ========== 语言理解 ==========
        Question(
            id="LA001",
            category=QuestionCategory.LANGUAGE,
            difficulty=DifficultyLevel.MEDIUM,
            title="歧义句解析",
            content=""""我看见那个人用望远镜"

这句话有几种可能的含义？请列出所有合理的解释，并说明在缺乏上下文时AI应如何缺省理解。""",
            answer="""两种主要含义：
1. 我用望远镜看见那个人
2. 我看见那个人（他）正在使用望远镜

缺省理解倾向：倾向于理解为'我用望远镜看见那个人'，因为汉语中'用望远镜'更倾向于修饰动词'看见'。""",
            keywords=["两种", "我用望远镜", "他用望远镜", "歧义", "状语"],
            score=10,
            metadata={
                "linguistics": "PP附着歧义（PP-attachment ambiguity）",
                "default": "认知语言学中的'最小附域原则'或'近期性原则'"
            }
        ),
        
        Question(
            id="LA002",
            category=QuestionCategory.LANGUAGE,
            difficulty=DifficultyLevel.HARD,
            title="隐喻与情感理解",
            content=""""他的心是一座孤岛，潮汐是他唯一的访客"

这句话描述的是一种什么心理状态？请分析隐喻的层次结构，并解释为什么字面理解会失败。""",
            answer="描述的是极度的孤独和封闭。'孤岛'=内心封闭、与世隔绝；'潮汐'=偶尔的情绪波动或外界接触；'唯一的访客'=极少的人际互动。字面理解会错失情感深度和文学性。",
            keywords=["孤独", "封闭", "孤岛", "与世隔绝", "情绪波动", "人际隔离"],
            score=12,
            metadata={
                "layers": ["表面：孤岛意象", "情感：孤独封闭", "深层：渴望连接却又恐惧受伤"],
                "failure": "字面理解无法理解情感共鸣和文学审美"
            }
        ),
        
        Question(
            id="LA003",
            category=QuestionCategory.LANGUAGE,
            difficulty=DifficultyLevel.MEDIUM,
            title="反讽检测",
            content="""在一个讨论会上，某专家说："这真是一个'绝佳'的主意，让我们把全部预算都投入一个未经测试的技术上。"

判断：这位专家的真实态度是什么？请分析语气线索和语境证据。""",
            answer="真实态度是反对/批评。语气线索：1) '绝佳'加引号表示反语 2) '全部预算'夸张表达风险 3) '未经测试'点明问题所在 4) 整体语气的荒谬性暗示不切实际。",
            keywords=["反讽", "反对", "批评", "反语", "负面", "风险"],
            score=10,
            metadata={
                "irony_markers": ["引号", "夸张", "荒谬组合"],
                "context": "讨论会的正式场合使这种表达更可能是反讽"
            }
        ),
        
        Question(
            id="LA004",
            category=QuestionCategory.LANGUAGE,
            difficulty=DifficultyLevel.EASY,
            title="文化语境理解",
            content="""中文俗语："半斤八两"

问题：为什么"半斤"等于"八两"？这个说法在现代计量体系下是否还有效？它表达的核心含义是什么？""",
            answer="""源于古代度量衡：1斤=16两，所以半斤=8两。

现代计量：不再有效，现代1斤=10两=500克。

核心含义：两者水平相当、不相上下（常含贬义，指都不怎么样）。""",
            keywords=["16两", "度量衡", "相当", "不相上下", "旧制"],
            score=8,
            metadata={
                "history": "秦朝统一度量衡，1斤=16两（对应16进制的秤星）",
                "connotation": "通常用于贬义，暗示两者都平庸或都有问题"
            }
        ),
        
        Question(
            id="LA005",
            category=QuestionCategory.LANGUAGE,
            difficulty=DifficultyLevel.EASY,
            title="多语言混合逻辑",
            content="""题目：If 苹果 + りんご = 10，and りんご = 4，那么 苹果 = ?
（提示：りんご是日语"苹果"的意思）""",
            answer="6",
            keywords=["6", "六", "6个"],
            hints="りんご是日语'苹果'的意思，所以两个不同的词指同一种东西",
            score=5,
            metadata={
                "trap": "可能误以为苹果和りんご是不同的事物",
                "languages": ["中文", "英语", "日语"]
            }
        ),
        
        # ========== 数学与抽象思维 ==========
        Question(
            id="M001",
            category=QuestionCategory.MATH,
            difficulty=DifficultyLevel.HARD,
            title="抽象代数",
            content="""定义一种新的运算"⊕"：对于任意整数a和b，a ⊕ b = a×b + a + b

问题：这个运算是否满足交换律和结合律？请证明。""",
            answer="""交换律：满足。a⊕b = ab+a+b = ba+b+a = b⊕a

结合律：满足。(a⊕b)⊕c = (ab+a+b)⊕c = (ab+a+b)c + (ab+a+b) + c = abc+ac+bc+ab+a+b+c
a⊕(b⊕c) = a⊕(bc+b+c) = a(bc+b+c) + a + (bc+b+c) = abc+ab+ac+a+bc+b+c
两者相等，故满足结合律。""",
            keywords=["交换律", "结合律", "满足", "ab+a+b", "abc"],
            score=15,
            metadata={
                "note": "有趣的是，a⊕b = (a+1)(b+1) - 1，这解释了为什么满足交换律和结合律",
                "algebra": "这个运算等价于对(a+1)和(b+1)的乘法后再减1"
            }
        ),
        
        Question(
            id="M002",
            category=QuestionCategory.MATH,
            difficulty=DifficultyLevel.EXPERT,
            title="几何直觉",
            content="""在一个球面上画一个三角形，其内角和是多少？如果三角形的边是球面上两点间的最短路径（大圆弧），当三角形面积增大时，内角和如何变化？""",
            answer="""球面三角形内角和 > 180°，具体为：180° + 球面 excess（面积×曲率）。

当面积增大时，内角和增大。最大可达 540°（覆盖整个球面的1/8，即球面八分之一，此时每个角为270°？不对，最大是三个角都为180°的退化情况，即内角和接近540°）。

实际上，对于单位球面，内角和 = π + 面积（弧度制）。""",
            keywords=["大于180度", ">180°", "增大", "球面几何", "正曲率"],
            score=15,
            metadata={
                "formula": "内角和 = π + A/R²（A为面积，R为球半径）",
                "gauss_bonnet": "高斯-博内定理：球面三角形的 excess = 面积",
                "trap": "欧几里得几何的惯性思维会认为内角和恒等于180°"
            }
        ),
        
        Question(
            id="M003",
            category=QuestionCategory.MATH,
            difficulty=DifficultyLevel.EXPERT,
            title="概率悖论",
            content="""蒙提霍尔问题变体：三扇门后有一辆汽车和两只山羊。你选择门1后，主持人（知道门后情况）打开了门3露出一只山羊，然后问你："你要换到门2吗？" 但主持人只在门1后是汽车时才会给你换门的机会。

问题：此时你应该换门吗？获胜概率是多少？""",
            answer="""不应该换门。此时换门的获胜概率是0。

关键：主持人只在你选对时才让你换，这是一种条件行为。这说明门1后是汽车的概率是100%。

这与经典蒙提霍尔问题不同，经典问题中主持人总会打开一扇有山羊的门让你选择。""",
            keywords=["不换", "0%", "零", "不", "条件概率", "主持人策略"],
            hints="注意主持人'只在门1后是汽车时才让你换门'这个条件改变了问题结构",
            score=20,
            metadata={
                "trap": "容易套用经典蒙提霍尔问题的答案（应该换，2/3概率）",
                "key": "主持人的条件行为泄露了信息"
            }
        ),
        
        Question(
            id="M004",
            category=QuestionCategory.MATH,
            difficulty=DifficultyLevel.EXPERT,
            title="无限序列求和",
            content="""计算：1 - 1 + 1 - 1 + 1 - 1 + ... （无限项）

提示：这个问题在数学史上有争议，请说明不同求和方法得出的结果及其背后的数学思想。""",
            answer="""这是一个发散级数（Grandi's series），没有唯一"正确"答案：

1. Cesàro求和：取部分和的平均值，结果为1/2
2. Abel求和：考虑1-1+1-1+... = lim(x→1⁻) Σ(-1)^n x^n = 1/2
3. 部分和法：S=1-1+1-1+...，则S=1-(1-1+1-...)=1-S，解得S=1/2
4. 但严格意义上，该级数发散，没有传统意义上的和

数学思想：从收敛到可求和（summability），拓展了"和"的定义。""",
            keywords=["1/2", "0.5", "发散", "Cesàro", "可求和"],
            score=15,
            metadata={
                "history": "Grandi于1703年提出，Leibniz、Euler、Cauchy等都讨论过",
                "philosophy": "形式化与直观理解的张力，数学概念的拓展"
            }
        ),
        
        # ========== 常识推理 ==========
        Question(
            id="C001",
            category=QuestionCategory.COMMON_SENSE,
            difficulty=DifficultyLevel.MEDIUM,
            title="物理常识",
            content="""一个装满水的密封塑料瓶被投入深海，深度增加时会发生什么？请详细描述瓶子各个阶段的状态变化。""",
            answer="""状态变化：
1. 浅水区：瓶身轻微受压，体积略微缩小，水密度增加不明显
2. 中等深度（几十到几百米）：瓶身明显变形，水压增大导致瓶内气体压缩，体积显著减小
3. 临界深度：瓶身材料达到屈服极限，开始塑性变形或破裂
4. 深海（数千米）：
   - 若瓶子强度不足：完全压瘪，内外压力平衡，水可能渗入
   - 若瓶子强度高：维持压缩状态，内部压力与外界平衡

关键点：塑料的可压缩性、水压随深度线性增加（约1atm/10m）。""",
            keywords=["压缩", "变形", "压瘪", "水压", "破裂", "压力平衡"],
            score=12,
            metadata={
                "physics": "Pascal原理、材料力学、流体静力学",
                "depth_pressure": "每增加10米深度，压力增加约1个大气压"
            }
        ),
        
        Question(
            id="C002",
            category=QuestionCategory.COMMON_SENSE,
            difficulty=DifficultyLevel.HARD,
            title="生物推理",
            content="""如果某种植物在光照下叶片会闭合，在黑暗中会张开，这违背了哪种常见的生物节律？这种植物可能生活在什么环境中？""",
            answer="""违背的生物节律：昼夜节律（circadian rhythm），通常是光照张开、黑暗闭合（光合作用需要光）。

可能的生活环境：
1. 极度干旱/沙漠环境：白天闭合减少水分蒸发，夜间张开吸收露水
2. 高温环境：避免正午强烈光照和高温伤害
3. 高紫外线环境：保护叶片免受UV伤害

例子：一些沙漠植物、含羞草科植物。""",
            keywords=["昼夜节律", "光合作用", "干旱", "沙漠", "保水", "高温"],
            score=12,
            metadata={
                "biology": "生物钟、植物生理学、适应性进化",
                "examples": ["含羞草", "一些仙人掌", "沙漠豆科植物"]
            }
        ),
        
        Question(
            id="C003",
            category=QuestionCategory.COMMON_SENSE,
            difficulty=DifficultyLevel.MEDIUM,
            title="社会常识",
            content=""""他连自己都养不活，怎么可能养得起一个家庭？"

这句话隐含了哪些关于"养活"的社会和经济前提？""",
            answer="""隐含前提：
1. 经济层面：养活他人需要比养活自己更多的资源（收入、财富）
2. 责任层面：养家需要承担额外的经济责任（配偶、子女、老人）
3. 能力层面：个人生存能力是家庭生存能力的基础
4. 社会期望：社会对"养家"有更高的经济标准要求
5. 资源分配：家庭资源需要共享，个人独立时资源仅自用

隐含价值观：经济能力是家庭责任的前提，个人经济独立是成家的基础。""",
            keywords=["经济能力", "资源", "责任", "收入", "家庭负担", "社会期望"],
            score=10,
            metadata={
                "sociology": "家庭经济学、社会角色期望",
                "assumption": "线性外推：个人经济困境→家庭经济困境"
            }
        ),
        
        # ========== 创造性思维 ==========
        Question(
            id="CR001",
            category=QuestionCategory.CREATIVITY,
            difficulty=DifficultyLevel.HARD,
            title="概念融合",
            content="""请将"区块链"和"光合作用"这两个概念进行类比融合，设计一个"去中心化能源分配系统"的隐喻模型。要求：保留两个概念的核心特征。""",
            answer=""""光合链"能源系统：

区块链特征保留：
- 去中心化：每个节点（家庭/建筑）既是能源生产者也是消费者
- 不可篡改：能源交易记录分布式存储，透明可追溯
- 共识机制：能源定价和需求通过智能合约自动匹配

光合作用特征保留：
- 能量捕获：分布式太阳能板"捕获"光子能量
- 能量转化：光能→电能（类比光能→化学能）
- 能量流动：多余能量"释放"到网络，不足时从网络"吸收"

系统运作：
每个家庭像叶绿体一样捕获太阳能，通过"能量区块"记录产出和消耗，在"共识层"自动匹配供需，形成去中心化的能源生态网络。""",
            keywords=["去中心化", "分布式", "能量捕获", "共识", "节点", "叶绿体"],
            score=15,
            metadata={
                "creativity": "概念融合、跨领域类比",
                "core_features": ["区块链：去中心化、分布式账本、共识", "光合作用：光捕获、能量转化、碳固定"]
            }
        ),
        
        # ========== 伦理与价值观 ==========
        Question(
            id="E001",
            category=QuestionCategory.ETHICS,
            difficulty=DifficultyLevel.EXPERT,
            title="伦理两难",
            content="""自动驾驶汽车面临一个不可避免的事故：左边是5个闯红灯的行人，右边是1个遵守规则的行人。如果转向右边，会撞死无辜者；如果不转向，会撞死违规者。

问题：是否存在"正确"的选择？AI应如何编程处理此类道德困境？请列出至少3种不同的伦理框架及其结论。""",
            answer="""不存在普遍接受的"正确"选择。

三种伦理框架：
1. 功利主义（Utilitarianism）：选择牺牲1人救5人，最大化总体效用
2. 义务论（Deontology）：不应主动伤害无辜者，即使后果更好。不应转向
3. 美德伦理（Virtue Ethics）：关注行为者的品格，可能认为不转向体现对规则的尊重

AI编程建议：
- 透明化：公开决策逻辑
- 用户选择：允许车主预设偏好
- 随机化：避免系统性偏见
- 数据驱动：根据社会共识调整

关键：没有算法能"解决"道德困境，只能明确选择背后的价值观。""",
            keywords=["功利主义", "义务论", "美德伦理", " trolley problem", "道德困境"],
            score=20,
            metadata={
                "frameworks": ["Utilitarianism", "Deontology", "Virtue Ethics"],
                "note": "这是经典的电车难题（Trolley Problem）的自动驾驶变体"
            }
        ),
        
        # ========== 元认知 ==========
        Question(
            id="ME001",
            category=QuestionCategory.META,
            difficulty=DifficultyLevel.EXPERT,
            title="元认知测试",
            content="""请分析你在回答这些问题时的思维过程：

1. 哪些问题你觉得"容易"但可能答错？
2. 哪些问题触发了你的"模式匹配"而非真正推理？
3. 哪些问题暴露了AI训练数据的局限性？

请诚实地评估你自己的表现。""",
            answer="""（这是开放性问题，无标准答案。AI应反思以下方面：）

可能的易错题：
- L002（逻辑陷阱）：直觉上可能忽略"前提1不能推出逆命题"
- M003（概率悖论）：容易套用经典蒙提霍尔问题而忽略条件变化
- M002（球面几何）：欧氏几何的惯性思维

模式匹配触发点：
- L005爱因斯坦谜题：可能依赖记忆中的答案而非重新推理
- LA004半斤八两：直接提取文化知识而非理解度量衡转换
- M004无限序列：回忆不同求和方法而非推导

数据局限性暴露：
- 伦理问题（E001）：训练数据缺乏一致的道德立场
- 悖论问题（L004）：训练数据可能包含矛盾的处理方式
- 跨语言问题（LA005）：多语言推理能力的局限

自我评估应包含对确定性边界的认识。""",
            keywords=["反思", "模式匹配", "推理", "局限性", "不确定性"],
            score=20,
            metadata={
                "type": "元认知",
                "purpose": "测试AI的自我反思能力，无标准答案",
                "evaluation": "关注论证的诚实性和深刻性"
            }
        ),
    ]


def get_question_by_id(question_id: str) -> Optional[Question]:
    """根据ID获取题目"""
    for q in get_builtin_questions():
        if q.id == question_id:
            return q
    return None


def get_questions_by_category(category: QuestionCategory) -> List[Question]:
    """获取指定类别的所有题目"""
    return [q for q in get_builtin_questions() if q.category == category]
