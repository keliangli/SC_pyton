# ModelScope 全站量化类型分布统计（2026-03-09）

- 全部模型数：175269
- 识别为量化相关的模型数：35901
- 量化相关模型占比：20.4834%

## 主类别分布（互斥）

| 类别 | 数量 | 占全部模型 | 占量化模型 |
|---|---:|---:|---:|
| none | 139368 | 79.5166% | 388.2009% |
| gguf | 17325 | 9.8848% | 48.2577% |
| int3 | 4254 | 2.4271% | 11.8493% |
| int4 | 3116 | 1.7778% | 8.6794% |
| awq | 2004 | 1.1434% | 5.582% |
| gptq | 1900 | 1.084% | 5.2923% |
| int8 | 1674 | 0.9551% | 4.6628% |
| fp8 | 1500 | 0.8558% | 4.1782% |
| exl2 | 781 | 0.4456% | 2.1754% |
| q2 | 774 | 0.4416% | 2.1559% |
| quantized-unspecified | 628 | 0.3583% | 1.7493% |
| 6bit-generic | 560 | 0.3195% | 1.5598% |
| fp4 | 325 | 0.1854% | 0.9053% |
| 5bit-generic | 262 | 0.1495% | 0.7298% |
| q8 | 162 | 0.0924% | 0.4512% |
| q6 | 129 | 0.0736% | 0.3593% |
| q4 | 113 | 0.0645% | 0.3148% |
| hqq | 85 | 0.0485% | 0.2368% |
| int2 | 81 | 0.0462% | 0.2256% |
| q3 | 73 | 0.0417% | 0.2033% |

## 多标签分布（可重复计数）

| 类别 | 数量 | 占全部模型 | 占量化模型 | 示例 |
|---|---:|---:|---:|---|
| gguf | 17352 | 9.9002% | 48.3329% | unsloth/Qwen3.5-9B-GGUF; unsloth/Qwen3.5-27B-GGUF; LocoreMind/LocoOperator-4B |
| int3 | 5269 | 3.0062% | 14.6765% | DiffSynth-Studio/FLUX.1-Kontext-dev-lora-SuperOutpainting; kkdddd/Paper-cut; AImissyou/3D |
| int4 | 5076 | 2.8961% | 14.1389% | ZhipuAI/chatglm2-6b; Qwen/Qwen-72B-Chat-Int4; ZhipuAI/chatglm2-6b-int4 |
| 4bit-generic | 3567 | 2.0352% | 9.9357% | LLM-Research/glm-4-9b-chat-GGUF; FunAGI/Qwen2.5-Omni-7B-GPTQ-4bit; DavidWen2025/Qwen3-VL-8B-Instruct-4bit-GPTQ |
| int8 | 3094 | 1.7653% | 8.6181% | ruoying425/8bit; SUSUSUCK/8bitgirl; ModelE/8bit-qwen-image-edit-2 |
| 8bit-generic | 2309 | 1.3174% | 6.4316% | ruoying425/8bit; ModelE/8bit-qwen-image-edit-2; ruoying425/8bit-v1 |
| awq | 2004 | 1.1434% | 5.582% | Qwen/Qwen2.5-VL-72B-Instruct-AWQ; Qwen/Qwen2.5-VL-7B-Instruct-AWQ; Qwen/Qwen3-32B-AWQ |
| gptq | 1911 | 1.0903% | 5.323% | Qwen/Qwen1.5-14B-Chat-GPTQ-Int4; Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4; Qwen/Qwen1.5-7B-Chat-GPTQ-Int4 |
| 6bit-generic | 1544 | 0.8809% | 4.3007% | LLM-Research/glm-4-9b-chat-GGUF; okwinds/DeepSeek-R1-Distill-Qwen-32B-MLX-6bit; AI-ModelScope/WizardLM-2-7B-GGUF |
| fp8 | 1529 | 0.8724% | 4.2589% | MusePublic/Qwen-image-fp8; ONETranquil/F.1-dev-fp8; muse/Wan2.2-TI2V-5B-FP8 |
| 5bit-generic | 1234 | 0.7041% | 3.4372% | LLM-Research/glm-4-9b-chat-GGUF; AI-ModelScope/WizardLM-2-7B-GGUF; LLM-Research/Mistral-7B-Instruct-v0.3-GGUF |
| int1 | 1143 | 0.6521% | 3.1838% | HiDream-ai/HiDream-I1-Full; AI-ModelScope/bitnet-b1.58-2B-4T; mradermacher/Huihui-Qwen3-8B-abliterated-v2-i1-GGUF |
| int2 | 1093 | 0.6236% | 3.0445% | QWQ114514123/shenchaoweiba-w2; zzzzzz77777/Qversion2.0; lxqyyds/W2 |
| q2 | 813 | 0.4639% | 2.2646% | fg43ghhfd/mox-daoguo-Q2; bunny0628/Bunny-Embroidery-Q2; tangchuc0137/q2 |
| exl2 | 781 | 0.4456% | 2.1754% | bartowski/Code-Llama-3-8B-exl2; bartowski/Pantheon-RP-1.5-12b-Nemo-exl2; Eigeen/Xwin-LM-13B-V0.2-8bpw-exl2 |
| quantized-unspecified | 628 | 0.3583% | 1.7493% | axin9470/LOJ2.0; modelscope_mp_129362455/test1111quantized; CuteOwls666/BrightLeafBooks |
| q8 | 423 | 0.2413% | 1.1782% | yingda/gte-Qwen2-1.5B-instruct-GGUF; ggml-org/DeepSeek-R1-Distill-Qwen-32B-Q8_0-GGUF; swift/llama3-8b-agent-instruct-v2-GGUF |
| fp4 | 337 | 0.1923% | 0.9387% | nv-community/DeepSeek-R1-FP4; nv-community/Qwen3-30B-A3B-FP4; nv-community/Qwen3-235B-A22B-FP4 |
| q4 | 221 | 0.1261% | 0.6156% | CarbonAgent/llama-2-13b-chat.Q4; cjc1887415157/Tifa-Deepsex-14b-CoT-GGUF-Q4; zimageapp/z-image-turbo-q4 |
| q6 | 199 | 0.1135% | 0.5543% | nanyu693/Q6; Manojb/qwen2.5-coder-14b-instruct-q6_k.gguf; nightmedia/Tongyi-DeepResearch-30B-A3B-q6-hi-mlx |
| hqq | 85 | 0.0485% | 0.2368% | mobiuslabsgmbh/Llama-2-7b-chat-hf-4bit_g64-HQQ; PrunaAI/maicomputer-alpaca-native-HQQ-4bit-smashed; PrunaAI/ai21labs-AI21-Jamba-Reasoning-3B-HQQ-8bit-smashed |
| q3 | 79 | 0.0451% | 0.22% | xiiian/Q.3; z647799842/Q3; bunny0628/Bunny-Embroidery-Q3 |
| q5 | 64 | 0.0365% | 0.1783% | tangchuc0137/q5; nightmedia/unsloth-gpt-oss-120b-q5-hi-mlx; prithivMLmods/Qwen2.5-Coder-7B-GGUF |
| nf4 | 46 | 0.0262% | 0.1281% | livehouse/flux1-dev-bnb-nf4-v2; ai-modelscope/flux1-dev-bnb-nf4; cjc1887415157/flux1-nf4 |
| aqlm | 24 | 0.0137% | 0.0669% | TechxGenus-MS/deepseek-coder-7b-instruct-v1.5-AQLM; TechxGenus-MS/deepseek-coder-7b-base-v1.5-AQLM; AI-ModelScope/Llama-2-7b-AQLM-2Bit-1x16-hf |
| eetq | 3 | 0.0017% | 0.0084% | kernels-community/quantization-eetq; dphn/dolphin-2.9.2-qwen2-72b-eetq; cognitivecomputations/dolphin-2.9.2-qwen2-72b-eetq |

## 说明
- 统计口径基于列表接口可见字段：Name/ChineseName/Tags/OfficialTags/Libraries/Frameworks/ModelType/Description。
- multi_label_counts 为多标签统计，一个模型可能同时命中多个类别（例如 GGUF + q4）。
- primary_counts 为互斥主类别统计，每个模型只归到一个优先级最高的类别。
- 这不是官方 benchmark 统计，而是 ModelScope 全站模型命名/标签层面的量化类型分布统计。