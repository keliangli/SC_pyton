# ModelScope 量化模型统计（按 2026 taxonomy 重构）

- 全部模型数：175,300
- 识别为量化相关的模型数：34,688（19.7878%）
- 落入用户给定六大核心流派的模型数：24,135（占量化模型 69.5774%）

## 一、按核心流派统计

| 核心流派 | 数量 | 占全部模型 | 占量化模型 |
|---|---:|---:|---:|
| 一、下一代硬件原生标准 | 1,490 | 0.85% | 4.2954% |
| 二、全链路量化加速 | 465 | 0.2653% | 1.3405% |
| 三、权重压缩 (PTQ) | 4,754 | 2.7119% | 13.705% |
| 四、混合架构与边缘侧 | 17,310 | 9.8745% | 49.902% |
| 五、微调专属规范 | 41 | 0.0234% | 0.1182% |
| 六、极限压缩与未来架构 | 75 | 0.0428% | 0.2162% |
| 七、通用位宽命名（未明确算法） | 10,553 | 6.02% | 30.4226% |

## 二、按代表格式/技术统计

| 流派 | 代表格式/技术 | 量化对象 | 数量 | 占量化模型 | 示例 |
|---|---|---|---:|---:|---|
| 四、混合架构与边缘侧 | GGUF | 仅权重/混合 | 17,310 | 49.902% | unsloth/Qwen3.5-9B-GGUF; unsloth/Qwen3.5-27B-GGUF; LocoreMind/LocoOperator-4B |
| 七、通用位宽命名（未明确算法） | INT3 / 3-bit generic | 未明确 | 4,250 | 12.2521% | AImissyou/3D; VoidOc/flux_pop_mart_1; xxcdesign/3Dcartoon |
| 七、通用位宽命名（未明确算法） | INT4 / 4-bit generic | 未明确 | 2,752 | 7.9336% | ZhipuAI/chatglm2-6b; Qwen/Qwen-72B-Chat-Int4; ZhipuAI/chatglm2-6b-int4 |
| 三、权重压缩 (PTQ) | AWQ | 仅权重 | 2,000 | 5.7657% | Qwen/Qwen2.5-VL-72B-Instruct-AWQ; Qwen/Qwen2.5-VL-7B-Instruct-AWQ; Qwen/Qwen3-32B-AWQ |
| 三、权重压缩 (PTQ) | GPTQ | 仅权重 | 1,887 | 5.4399% | Qwen/Qwen1.5-14B-Chat-GPTQ-Int4; Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4; Qwen/Qwen1.5-7B-Chat-GPTQ-Int4 |
| 七、通用位宽命名（未明确算法） | INT8 / 8-bit generic | 未明确 | 1,599 | 4.6097% | ruoying425/8bit; ModelE/8bit-qwen-image-edit-2; ruoying425/8bit-v1 |
| 一、下一代硬件原生标准 | 标准 FP8 | 权重+激活 | 1,052 | 3.0327% | muse/Wan2.2-TI2V-5B-FP8; ONETranquil/F.1-dev-fp8; MusePublic/FLUX.1-dev-fp8-dit |
| 三、权重压缩 (PTQ) | EXL2 | 仅权重 | 781 | 2.2515% | bartowski/Code-Llama-3-8B-exl2; bartowski/Pantheon-RP-1.5-12b-Nemo-exl2; Eigeen/Xwin-LM-13B-V0.2-8bpw-exl2 |
| 七、通用位宽命名（未明确算法） | Q2 generic | 未明确 | 773 | 2.2284% | bunny0628/Bunny-Embroidery-Q2; tangchuc0137/q2; IceWindai/byna-Q2 |
| 七、通用位宽命名（未明确算法） | Quantized unspecified | 未明确 | 493 | 1.4212% | axin9470/LOJ2.0; modelscope_mp_129362455/test1111quantized; CuteOwls666/BrightLeafBooks |
| 二、全链路量化加速 | SmoothQuant / W8A8 | 权重+激活 | 465 | 1.3405% | neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w8a8; neuralmagic/DeepSeek-R1-Distill-Qwen-32B-quantized.w8a8; vllm-ascend/Qwen3-235B-A22B-W8A8 |
| 一、下一代硬件原生标准 | NVFP4 | 权重+激活 | 207 | 0.5967% | black-forest-labs/FLUX.2-klein-9b-nvfp4; lightx2v/Wan-NVFP4; AiMETATRON/FLUX.2-klein-9B-Blitz |
| 一、下一代硬件原生标准 | MXFP4 / MXFP6 | 权重+激活 | 206 | 0.5939% | hf/BennyDaBall-MiniMax-M2.5-REAP-139B-A10B-MXFP4; hf/GadflyII-GLM-4.7-Flash-MXFP4; nightmedia/Qwen3.5-122B-A10B-Text-mxfp4-mlx |
| 七、通用位宽命名（未明确算法） | Q8 generic | 未明确 | 164 | 0.4728% | mlx-community/FuseO1-DeepSeekR1-Qwen2.5-Coder-32B-Preview-Q8; xiaowangge/conan-embedding-v1-q8; nightmedia/Gemma3-27B-it-vl-HERETIC-GLM4.7-2200x-cp515-q8-mlx |
| 七、通用位宽命名（未明确算法） | Q6 generic | 未明确 | 129 | 0.3719% | nanyu693/Q6; nightmedia/Tongyi-DeepResearch-30B-A3B-q6-hi-mlx; nightmedia/Qwen3-Esper3-Reasoning-CODER-Instruct-21B-Brainstorm20x-q6-mlx |
| 七、通用位宽命名（未明确算法） | Q4 generic | 未明确 | 114 | 0.3286% | zimageapp/z-image-turbo-q4; google/gemma-3-270m-it-qat-q4_0-unquantized; google/embeddinggemma-300m-qat-q4_0-unquantized |
| 七、通用位宽命名（未明确算法） | FP4 generic | 未明确 | 89 | 0.2566% | nv-community/DeepSeek-R1-FP4; nv-community/Qwen3-30B-A3B-FP4; nv-community/Qwen3-235B-A22B-FP4 |
| 三、权重压缩 (PTQ) | HQQ | 仅权重 | 86 | 0.2479% | mobiuslabsgmbh/Llama-2-7b-chat-hf-4bit_g64-HQQ; PrunaAI/maicomputer-alpaca-native-HQQ-4bit-smashed; PrunaAI/ai21labs-AI21-Jamba-Reasoning-3B-HQQ-8bit-smashed |
| 七、通用位宽命名（未明确算法） | Q3 generic | 未明确 | 73 | 0.2104% | xiiian/Q.3; z647799842/Q3; bunny0628/Bunny-Embroidery-Q3 |
| 七、通用位宽命名（未明确算法） | INT2 / 2-bit generic | 未明确 | 62 | 0.1787% | QWQ114514123/shenchaoweiba-w2; zzzzzz77777/Qversion2.0; lxqyyds/W2 |
| 七、通用位宽命名（未明确算法） | Q5 generic | 未明确 | 55 | 0.1586% | tangchuc0137/q5; nightmedia/unsloth-gpt-oss-120b-q5-hi-mlx; nightmedia/LFM2-350M-Math-q5-hi-mlx |
| 六、极限压缩与未来架构 | BitNet b1.58 | 架构重构 | 46 | 0.1326% | AI-ModelScope/bitnet-b1.58-2B-4T; AI-ModelScope/bitnet-b1.58-2B-4T-bf16; microsoft/bitnet-b1.58-2B-4T |
| 五、微调专属规范 | NF4 | 仅权重 | 41 | 0.1182% | livehouse/flux1-dev-bnb-nf4-v2; ai-modelscope/flux1-dev-bnb-nf4; cjc1887415157/flux1-nf4 |
| 六、极限压缩与未来架构 | AQLM / QuIP# | 仅权重 | 29 | 0.0836% | TechxGenus-MS/deepseek-coder-7b-instruct-v1.5-AQLM; TechxGenus-MS/deepseek-coder-7b-base-v1.5-AQLM; AI-ModelScope/Llama-2-7b-AQLM-2Bit-1x16-hf |
| 一、下一代硬件原生标准 | MXFP8 / MXINT8 | 权重+激活 | 25 | 0.0721% | nightmedia/Qwen3.5-27B-Claude-4.6-OS-INSTRUCT-mxfp8-mlx; nightmedia/Qwen3.5-2B-mxfp8-mlx; nightmedia/Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-mxfp8-mlx |

## 三、按量化对象统计

| 量化对象 | 数量 | 占量化模型 |
|---|---:|---:|
| 仅权重/混合 | 17,310 | 49.902% |
| 未明确 | 10,553 | 30.4226% |
| 仅权重 | 4,824 | 13.9068% |
| 权重+激活 | 1,955 | 5.636% |
| 架构重构 | 46 | 0.1326% |

## 四、结果解读

- 在你给定的 taxonomy 下，**GGUF** 依然是 ModelScope 上最显著的发布形态，数量为 **17,310**。
- **AWQ + GPTQ + HQQ + EXL2** 这类典型“权重压缩 PTQ”合计 **4,754**，占量化模型 **13.705%**。
- **FP8 / MXFP / NVFP4 / SmoothQuant-W8A8** 代表的“硬件原生/全链路”路线，在 ModelScope 的公开模型命名层面总量仍明显小于 GGUF/AWQ/GPTQ。
- 有 **10,553** 个量化模型没有明确暴露你给定 taxonomy 里的具体算法名，而是以 int3/int4/q4/8bit 等**通用位宽命名**存在；这说明社区发布命名习惯仍偏“格式/位宽导向”，而非统一按算法名命名。

## 五、说明与局限
- 本统计基于 ModelScope 列表接口字段（Name/ChineseName/Tags/OfficialTags/Libraries/Frameworks/ModelType/Description）做规则匹配，不读取 README 全文。
- 为了贴合用户给定 taxonomy，报告保留六大核心流派；同时新增“七、通用位宽命名（未明确算法）”作为补充类，用于承接 int3/int4/q4/8bit 等没有明确算法名的模型。
- “标准 FP8”实际是从命名和标签中识别的 FP8 / E4M3 / E5M2；无法完全区分其是否为用户文中所述硬件原生标准实现。
- “SmoothQuant / W8A8”采用名称关键词近似识别；只写 W8A8 的模型不一定严格等价于 SmoothQuant。
- GGUF 这里被放在“混合架构与边缘侧”；它在工程上更偏封装/生态格式，不完全等同于某一种底层量化算法。