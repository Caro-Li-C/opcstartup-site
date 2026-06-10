---
layout: post
title: “华为"韬定律”：多层电子系统的时间缩放理论"
date: 2026-05-28 00:00:00 +0800
category: 原文速递
read_time: 30
views: "[待确认]"
original_url: "[待补充]"
description: "华为提出τ缩放定律，以时间常数τ取代晶体管面积作为半导体进步的首要度量，展示LogicFolding与AI数据中心架构的量产验证。"
tags: ["华为", "半导体", "τ缩放", "摩尔定律", "LogicFolding", "AI基础设施"]
author: "OPC创业汇"
source: "公众号OPC创业汇"
---

> **原文标题**：A Time Scaling Theory for Multi-Layer Electronic Systems  
> **作者**：Tingbo He / 何庭波  
> **机构**：Huawei / 华为

---

<div class="bilingual-block">
<p class="en-text">For six decades, Moore's geometric scaling drove progress in semiconductors. That industry compact no longer holds: returns from pure dimensional shrinking have flattened, leading-edge design budgets exceed one billion dollars per chip, and cost-per-transistor at the most advanced nodes is no longer falling. This perspective argues for a successor scaling principle — τ scaling — that adopts time itself, rather than transistor area, as the primary metric of progress, applying a single characteristic time constant τ as the unifying optimization target across twelve orders of magnitude, from a switching transistor to a data-center workload. Two production-scale demonstrations are presented. On a mobile SoC, LogicFolding delivers a 55% stepwise increase in transistor density and a 41% power-efficiency gain at a fixed device node. On AI systems, a co-designed stack comprising the memory-semantic Unified Bus fabric, near-packaged Hi-ONE optical I/O, and edge-to-surface 3D Folding projects more than 100× growth in hardware integration by 2035. The deeper claim is methodological: τ scaling is the first scaling principle since Dennard to establish a shared optimization target across the entire computing stack.</p>
<p class="zh-text">六十年来，摩尔的几何缩放驱动了半导体产业的进步。但这一行业共识已不再成立：纯粹尺寸微缩的收益已经趋平，前沿芯片的设计预算超过每颗十亿美元，最先进节点的单晶体管成本不再下降。本文提出了一种继任的缩放原理——τ缩放——它将时间本身，而非晶体管面积，作为进步的首要度量标准，以一个单一的特征时间常数τ作为统一优化目标，跨越十二个数量级。文中展示了两个量产级验证案例。在移动SoC上，LogicFolding在固定器件节点下实现了晶体管密度55%的阶梯式提升和功耗效率41%的增益。在AI系统上，预计到2035年实现硬件集成度超过100倍的增长。更深层的论断是方法论层面的：τ缩放是自登纳德缩放以来第一个为整个计算栈建立共享优化目标的缩放原理。</p>
</div>

## § Lead / 导言

<div class="bilingual-block">
<p class="en-text">Since the mid-1960s, the semiconductor industry has measured progress in nanometers. Every eighteen months, transistors shrank, frequencies rose, and the cost per logic gate fell. Moore's Law functioned as both an empirical observation and helped establish an industry compact upon which the entire computing stack was built. That industry compact no longer holds. Beyond the 7 nm node, geometric scaling no longer delivers its historical dividends. Lithography tooling is approaching the physical limits of patterning, EUV depreciation dominates wafer cost, and the per-transistor price curve has flattened — and in some cases reversed.</p>
<p class="zh-text">自1960年代中期以来，半导体产业一直以纳米为单位衡量进步。每隔十八个月，晶体管缩小，频率提升，每个逻辑门的成本下降。摩尔定律既是一种经验观察，也帮助建立了一种行业共识，整个计算栈都建立在这一契约之上。但这一行业共识已不再成立。越过7纳米节点之后，几何缩放不再提供其历史性的红利。光刻工具正逼近图形化的物理极限，EUV折旧主导了晶圆成本，单晶体管价格曲线已经趋平——甚至在某些情况下出现反转。</p>
</div>

<div class="bilingual-block">
<p class="en-text">The central question for the industry has therefore changed. It is no longer "how much further can the transistor shrink?" It is "what should be scaled, and against what objective?"</p>
<p class="zh-text">因此，产业的核心问题已经改变。它不再是"晶体管还能缩小多少？"而是"应该缩放什么，以及以什么为目标？"</p>
</div>

<div class="bilingual-block">
<p class="en-text">Over the past six years, the author's team at Huawei Semiconductor has investigated this question in silicon across mobile SoCs, AI accelerators, system fabrics, and packaging. The conclusion is that the answer lies not in another node, nor in another transistor architecture, but in a change of the primary optimization target itself. This perspective argues that the next decade of electronic-system evolution should be guided not by geometric scaling, but by time scaling — the systematic reduction of a single characteristic time constant τ across every layer of the stack, from a transistor switching in a picosecond to a data-center workload responding in a second.</p>
<p class="zh-text">在过去六年中，作者所在的华为半导体团队在移动SoC、AI加速器、系统互连架构和封装领域的硅片实践中研究了这一问题。结论是，答案不在于另一个节点，也不在于另一种晶体管架构，而在于主要优化目标本身的改变。本文认为，未来十年电子系统的演进不应由几何缩放引导，而应由时间缩放引导——系统性地降低整个栈每一层的单一特征时间常数τ，从皮秒级开关的晶体管到秒级响应的数据中心工作负载。</p>
</div>

## § 1. The End of the Geometric Era
## § 1. 几何时代的终结

<div class="bilingual-block">
<p class="en-text">For most of its history, the semiconductor industry has had one job: make the transistor smaller. Gordon Moore's 1965 observation — that transistor density doubles approximately every two years — was complemented a decade later by Robert Dennard's scaling theory, which established that proportional shrinking of voltage and dimensions could maintain a constant electric field. Together, geometric scaling and Dennard scaling delivered exponential improvements in performance per watt and performance per dollar for nearly five decades.</p>
<p class="zh-text">在半导体产业的大部分历史中，它只有一个任务：让晶体管更小。戈登·摩尔1965年的观察——晶体管密度大约每两年翻一番——在十年后被罗伯特·登纳德的缩放理论所补充，该理论确立了电压和尺寸的等比例缩小可以维持恒定电场。几何缩放与登纳德缩放共同作用，在近五十年里带来了每瓦性能和每美元性能的指数级提升。</p>
</div>

<div class="bilingual-block">
<p class="en-text">This arrangement unraveled in two stages. Around 2005, Dennard scaling broke first: voltage ceased to scale proportionally with feature size, and the dark-silicon era began. Geometric scaling persisted longer, sustained by FinFET and subsequently gate-all-around (GAA) device architectures. Beyond 7nm, however, returns from pure dimensional scaling have flattened. The reasons are now well documented: velocity saturation reduces the dependence of intrinsic delay on channel length from quadratic to linear; the parasitic resistance and capacitance of local interconnects increasingly dominate the standard-cell delay budget; mask costs, EUV depreciation, and design-rule complexity have driven leading-edge chip design budgets past one billion dollars per chip at the 2 nm node.</p>
<p class="zh-text">这一格局分两个阶段解体。大约在2005年，登纳德缩放首先崩盘：电压不再与特征尺寸成比例缩放，暗硅时代由此开始。几何缩放持续得久一些，主要是由FinFET及随后的全环绕栅极（GAA）器件架构所支撑。然而，越过7纳米之后，纯粹尺寸微缩的收益已经趋平。原因现已得到充分确认：速度饱和将本征延迟对沟道长度的依赖从二次方降低为线性；局部互连的寄生电阻和电容日益主导标准单元的延迟预算；掩膜成本、EUV折旧和设计规则复杂性已将前沿芯片的设计预算在2纳米节点推高至每颗超过十亿美元。</p>
</div>

<div class="bilingual-block">
<p class="en-text">The economic consequences are equally inescapable. Cost per transistor has flattened at advanced nodes and, at the leading edge, is now rising. The industry compact that sustained the last fifty years — more transistors at lower cost every generation — no longer holds.</p>
<p class="zh-text">经济后果同样不可避免。先进节点的单晶体管成本已经趋平，而在最前沿，现在正在上升。支撑了过去五十年的行业共识——每一代以更低成本获得更多晶体管——已不再成立。</p>
</div>

<div class="bilingual-block">
<p class="en-text">For Huawei Semiconductor, this transition arrived with an additional constraint: restricted access to the most advanced lithography tooling. Assuming that another node would resolve the problem was no longer tenable. Six years ago, the geometric roadmap plateaued, forcing a more fundamental question — one that, in retrospect, the entire industry will eventually have to confront.</p>
<p class="zh-text">对于华为半导体而言，这一转变伴随着一个额外约束：对最先进光刻工具的获取受到限制。再推进一个节点就能解决问题的假设已不再成立。六年前，几何微缩的技术路线图陷入停滞，由此引出了一个更为根本性的问题——这个问题，事后看来，整个行业终将无法回避。</p>
</div>

## § 2. Time, Not Space
## § 2. 时间，而非空间

<div class="bilingual-block">
<p class="en-text">Reduced to its essential effect on the end user, Moore's Law was never fundamentally about geometry. Smaller transistors improved system performance because they switched faster. Denser interconnects improved performance because signals traversed shorter distances. Higher integration improved performance because data crossed fewer boundaries. What each generation delivered, in essence, was a reduction in time — picosecond to nanosecond at the device, nanosecond to microsecond at the chip, microsecond to second at the system. Spatial scaling served merely as the instrument for compressing time.</p>
<p class="zh-text">若将其对终端用户的核心效应加以提炼，摩尔定律在根本上从来不是关于几何的。更小的晶体管提升了系统性能，因为它们开关得更快。更密集的互连提升了性能，因为信号传输的距离更短。更高的集成度提升了性能，因为数据跨越的边界更少。每一代本质上交付的，都是时间的缩减——器件层面从皮秒到纳秒，芯片层面从纳秒到微秒，系统层面从微秒到秒。空间缩放仅仅是压缩时间的工具。</p>
</div>

<div class="bilingual-block">
<p class="en-text">Once this is recognized, an obvious reframing presents itself. Time itself should be adopted as the primary metric. A characteristic time constant τ can be defined at every layer of the stack — transistor, circuit, chip, and system — and its reduction treated as the unifying optimization target. Geometric scaling then becomes one technique among many for reducing τ, rather than the only one.</p>
<p class="zh-text">一旦认识到这一点，一种显而易见的重新界定便自然浮现：应当把时间本身作为首要度量指标。在技术栈的每一层——晶体管、电路、芯片和系统——都可以定义一个特征时间常数 τ，并将其缩短作为统一的优化目标。这样一来，几何微缩便只是缩短 τ 的众多方法之一，而不再是唯一的方法。</p>
</div>

<div class="bilingual-block">
<p class="en-text">τ = f(τ_transistor, τ_circuit, τ_chip, τ_system)</p>
<p class="zh-text">τ = f(τ_晶体管, τ_电路, τ_芯片, τ_系统)</p>
</div>

<div class="bilingual-block">
<p class="en-text">• Transistor: intrinsic switching delay, addressed through mobility enhancement, strain engineering, high-κ/metal gate, and GAA architectures.</p>
<p class="zh-text">• 晶体管：本征开关延迟，通过迁移率增强、应变工程、高κ/金属栅以及全环绕栅极（GAA）架构来解决。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• Circuit: RC propagation delay along signal paths, addressed through lower-resistivity conductors, low-κ dielectrics, and vertical integration.</p>
<p class="zh-text">• 电路：信号路径上的RC传播延迟，通过低电阻率导体、低κ介质以及垂直集成来解决。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• Chip: compute and memory-access latency, addressed through architectural choices, pipeline depth, memory hierarchy, and on-chip fabrics.</p>
<p class="zh-text">• 芯片：计算与存储访问延迟，通过架构选择、流水线深度、存储层级和片上互连架构来解决。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• System: end-to-end message and synchronization time, addressed through interconnect topology, protocol stack, and fabric design.</p>
<p class="zh-text">• 系统：端到端消息与同步时间，通过互连拓扑、协议栈和架构设计来解决。</p>
</div>

<div class="bilingual-block">
<p class="en-text">τ_{n+1} = τ_n / α</p>
<p class="zh-text">τ_{n+1} = τ_n / α</p>
</div>

<div class="bilingual-block">
<p class="en-text">where the scaling factor α is application-specific rather than universal. Production experience to date indicates α ≈ 1.3× per year for power-constrained mobile devices, ≈ 1.5× per year for safety-critical autonomous systems, and up to 10× per year for AI workloads, where throughput translates directly into economic value.</p>
<p class="zh-text">其中缩放因子α是应用特定的，而非普适的。迄今为止的量产经验表明，对于受功耗约束的移动设备，α约为每年1.3倍；对于安全关键型自动驾驶系统，约为每年1.5倍；对于AI工作负载，可达每年10倍——在AI场景中，吞吐量直接转化为经济价值。</p>
</div>

<div class="bilingual-block">
<p class="en-text">What renders τ a useful primary metric, rather than a relabeling of existing ones, is that it is the same metric across the entire stack. Frequency, latency, bandwidth, and throughput are all governed by τ at their respective layers. A process technologist, a circuit designer, and a system architect can debate the same quantity in identical units. τ is the language that enables end-to-end stack co-optimization — and the era of independent optimization at each layer, with timing emerging as a residual, has concluded.</p>
<p class="zh-text">τ之所以是一个有用的首要度量指标，而非仅仅给既有指标换了个标签，原因在于它在整个技术栈中是统一的度量。频率、延迟、带宽和吞吐量在其所在层级都由τ所支配。工艺技术专家、电路设计师和系统架构师可以用相同的单位争论同一个量。τ是一种语言，它使得端到端的栈协同优化成为可能——而每一层独立优化、时序作为残余结果出现的时代，已经终结。</p>
</div>

## § 3. LogicFolding
## § 3. 逻辑折叠

<div class="bilingual-block">
<p class="en-text">The first production-scale test of τ scaling was conducted in mobile. A smartphone SoC is the unusual case in which one chip constitutes the entire system. Multi-socket parallelism is not available; no thousand-node fabric can mask a slow link. All performance delivered to the user originates from a single die, under a few-watt power envelope, against thermal limits set by handheld form-factor constraints.</p>
<p class="zh-text">τ缩放的首次量产级检验是在移动领域进行的。智能手机SoC的特殊之处在于，单颗芯片即构成整个系统。这里无法诉诸多插槽并行，也没有上千节点的互连结构来掩盖某条慢速链路。交付给用户的全部性能都源于单一裸片，受限于几瓦的功耗包络，并须直面手持设备外形尺寸所决定的散热极限。</p>
</div>

<div class="bilingual-block">
<p class="en-text">LogicFolding is a design methodology that partitions digital, analog, and memory circuits across vertically stacked active tiers to jointly optimize performance, power, and area following the time scaling principle.</p>
<p class="zh-text">LogicFolding 是一种设计方法，它遵循时间缩放原则，将数字、模拟和存储电路划分到垂直堆叠的有源层上，以协同优化性能、功耗与面积。</p>
</div>

<div class="bilingual-block">
<p class="en-text">LogicFolding abandons the planar assumption. Critical-path gates are distributed across two (and eventually more) vertically stacked active tiers, connected through ultra-fine-pitch hybrid bonding. From the circuit designer's perspective, the two tiers behave as a single continuous fabric, with cells distributed across the wafer boundary as if it were an additional metal layer. Signal wires become substantially shorter, parasitic RC decreases sharply, clock skew tightens, and the chip operates at a higher clock frequency at the same device node.</p>
<p class="zh-text">LogicFolding抛弃了平面假设。关键路径门单元被分布到两个（以及未来更多）垂直堆叠的有源层上，通过超细间距混合键合连接。从电路设计师的视角看，两层表现为一个单一连续的结构，单元分布在晶圆边界上，仿佛它是一个额外的金属层。信号线大幅缩短，寄生RC急剧下降，时钟偏斜收紧，芯片在相同器件节点下以更高的时钟频率运行。</p>
</div>

<div class="bilingual-block">
<p class="en-text">The results, measured on Kirin 2026, are concrete:</p>
<p class="zh-text">在Kirin 2026上测得的结果是具体的：</p>
</div>

<div class="bilingual-block">
<p class="en-text">• Transistor density rose step-wise from 155 to 238 MTr/mm² in a single generation — a magnitude of improvement that previously required three years of geometric scaling.</p>
<p class="zh-text">• 晶体管密度在一个代际内从155提升至238 MTr/mm²——这一改进幅度此前需要三年的几何缩放才能实现。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• SoC performance-core power efficiency improved by 41% and maximum clock frequency rose by nearly 13%.</p>
<p class="zh-text">• SoC性能核心的能效提升了41%，最大时钟频率提高了近13%。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• SRAM operating frequency increased by over 40%.</p>
<p class="zh-text">• SRAM工作频率提升了40%以上。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• Clock-buffer count reduced by more than 50%, clock skew by 25%, and wire length by approximately 30%.</p>
<p class="zh-text">• 时钟缓冲器数量减少了50%以上，时钟偏斜降低了25%，导线长度减少了约30%。</p>
</div>

## § 4. AI Data Center
## § 4. AI数据中心

<div class="bilingual-block">
<p class="en-text">A natural question is whether a principle developed in the milliwatt smartphone regime survives translation to the gigawatt regime of AI training and inference. AI workloads occupy the opposite end of the τ spectrum: not a single chip but hundreds or thousands of chips behaving as one machine, with aggregate compute increasing by approximately six orders of magnitude over the past decade.</p>
<p class="zh-text">一个自然的问题是：在毫瓦级智能手机领域发展起来的原理，能否迁移到吉瓦级AI训练与推理领域。AI工作负载占据τ谱系的另一端：不是单颗芯片，而是数百或数千颗芯片如同一台机器般协同工作，总算力在过去十年中增长了约六个数量级。</p>
</div>

<div class="bilingual-block">
<p class="en-text">Two facts shape the AI side of the τ argument. First, AI systems continue to grow — from one chip, to dozens, to hundreds, and increasingly to tens of thousands. Second, the energy budget and the materials budget of modern AI systems are dominated by data, not by compute. Over 80% of energy in a large AI cluster is consumed by data movement; over 70% of system cost is allocated to data storage.</p>
<p class="zh-text">两个事实塑造了τ论证在AI一侧的形态。第一，AI系统持续增长——从一颗芯片，到数十颗，到数百颗，乃至日益达到数万颗。第二，现代AI系统的能耗预算和材料预算由数据主导，而非计算。大型AI集群中超过80%的能耗被数据移动所消耗；超过70%的系统成本被分配给数据存储。</p>
</div>

<div class="bilingual-block">
<p class="en-text">τ scaling is instantiated at AI scale through three coordinated layers: a system fabric (Unified Bus), a near-packaged optical engine (Hi-ONE), and a topological reorganization of the package itself (3D Folding).</p>
<p class="zh-text">τ缩放在AI规模上通过三个协同层得以实现：一个系统互连架构（统一总线，Unified Bus）、一个近封装光引擎（Hi-ONE），以及封装本身的拓扑重组（3D折叠）。</p>
</div>

### 4.1 Unified Bus / 4.1 统一总线

<div class="bilingual-block">
<p class="en-text">Unified Bus (UB) replaces the traditional multi-protocol stack with a single protocol that operates within and across the chassis — a fully peer-to-peer fabric that exposes memory semantics natively across the whole system. The measured benefit is approximately two orders of magnitude: end-to-end remote-access latency falls from the tens of microseconds typical of TCP/IP-class stacks to approximately 100 ns — a ~500× reduction in system τ.</p>
<p class="zh-text">统一总线（UB）用一个在机箱内部和跨机箱运行的单一协议取代了这一堆栈——一个完全对等的互连架构，在整个系统中原生暴露内存语义。实测收益约为两个数量级：端到端远程访问延迟从TCP/IP类栈典型的数十微秒下降到约100纳秒——沿主导通信轴实现了约500倍的系统τ缩减。</p>
</div>

### 4.2 Hi-ONE / 4.2 Hi-ONE光互连

<div class="bilingual-block">
<p class="en-text">Hi-ONE (High-density Optical-interconnect-Node Engine) is a near-packaged optical engine that delivers 8 Tb/s per module, matching the UB bandwidth of an AI chip on a single optical link. It reduces the required SerDes reach from ~100cm to ~5 cm, eliminates bulky cabling, and extends reach from under a meter to 100 meters — rendering high-density interconnect for distributed, gigawatt-scale data centers physically realizable.</p>
<p class="zh-text">Hi-ONE（高密度光互连节点引擎）是一个近封装光引擎，每模块提供8 Tb/s带宽，在单条光链路上匹配AI芯片的UB带宽。它将所需的SerDes传输距离从约100厘米缩短到约5厘米，消除了笨重的线缆，并将传输距离从不足一米扩展到100米——使分布式、吉瓦级数据中心的高密度互连在物理上成为现实。</p>
</div>

### 4.3 3D Folding / 4.3 3D折叠

<div class="bilingual-block">
<p class="en-text">In a conventional 2.5D AI chip, compute capacity scales as N² (area), but memory bandwidth, interconnect, and power delivery — all carried by the 2.5D fan-out along the edge — scale only as N (perimeter). The widening divergence constitutes the fan-out dilemma. 3D Folding resolves this by relocating the edge-bound resources onto surfaces, restoring N² parity.</p>
<p class="zh-text">在传统的2.5D AI芯片中，计算容量按N²缩放（面积），但存储带宽、互连和供电——全部由沿边缘的2.5D扇出承载——仅按N缩放（周长）。这些二次方曲线与线性曲线之间日益扩大的分歧构成了扇出困境。3D折叠通过将边缘束缚的资源迁移到表面上来解决这一困境，恢复N²对等性。</p>
</div>

## § 5. Logic and Memory
## § 5. 逻辑与存储

<div class="bilingual-block">
<p class="en-text">In the 8086 era, the industry deliberately decoupled processors and memory through standardized memory buses. That decoupling permitted two industries to scale independently: processor performance advanced rapidly along the Moore curve, while memory vendors developed a vast, separate market alongside it. The AI era is reversing this decoupling. HBM, hybrid bonding, and 3D-stacked SRAM are symptoms of a single underlying fact: for modern AI workloads, data movement is as critical as computation itself, and logic and memory are once again being driven into tight physical integration.</p>
<p class="zh-text">在8086时代，产业通过标准化存储总线刻意将处理器与存储解耦。这一解耦使得两个产业能够独立缩放：处理器性能沿摩尔曲线快速提升，而存储厂商在其旁发展出一个庞大而独立的市场。AI时代正在逆转这一解耦。HBM、混合键合和3D堆叠SRAM都是同一个根本事实的症状：对于现代AI工作负载，数据移动与计算本身同等关键，逻辑与存储再次被驱动进入紧密的物理集成。</p>
</div>

## § 6. Open Challenges
## § 6. 开放挑战

<div class="bilingual-block">
<p class="en-text">Today's EDA was developed for an era in which area, timing, and power were optimized along three separate axes, with system τ emerging as a residual. Full-scale LogicFolding requires the toolchain to treat multiple stacked dies as a single continuous design entity. A τ-native toolchain — open, multi-physics, and 3D-native — is the single most important enabling investment for the next decade.</p>
<p class="zh-text">当今的EDA是为一个面积、时序和功耗沿三条独立轴进行优化的时代而开发的，系统τ作为残余结果出现。全规模LogicFolding要求工具链将多颗堆叠裸片视为一个单一连续的设计实体。一个τ原生工具链——开放的、多物理场的、三维原生的——是未来十年最重要的一项赋能投资。</p>
</div>

<div class="bilingual-block">
<p class="en-text">τ is a time law, not a joule law. A super-node operating 10× faster but with 10× greater power consumption violates no scaling principle, yet exceeds grid capacity. τ scaling therefore requires an energy companion: memory-semantic fabrics, near-/co-packaged optics, backside power delivery, compute-in-memory, and the disciplined practice of trading τ headroom back for power.</p>
<p class="zh-text">τ是时间定律，而非焦耳定律。一个运行速度快10倍但功耗也增加10倍的超级节点并不违反任何缩放原理，却会超出电网容量。因此τ缩放需要一个能量伴侣：消除堆栈开销的内存语义互连架构、将每比特皮焦耳降低数量级的近封装光学器件、背面供电、存内计算，以及将τ裕量换回功耗的实践。</p>
</div>

## § 7. Six Years In, Ten Years Out
## § 7. 六年已过，十年展望

<div class="bilingual-block">
<p class="en-text">Between May 2020 and May 2026, Huawei Semiconductor designed and brought to volume production 381 chips serving mobile, AI, automotive, industrial, and infrastructure markets. Across that portfolio, the τ scaling thesis has held up:</p>
<p class="zh-text">从2020年5月到2026年5月，华为半导体设计并量产交付了381颗芯片，服务于移动、AI、汽车、工业和基础设施市场。在整个产品组合中，τ缩放论题已经得到验证：</p>
</div>

<div class="bilingual-block">
<p class="en-text">• At the device and circuit layers, transistor density has risen from 155 toward 400+ MTr/mm² by 2031.</p>
<p class="zh-text">• 在器件和电路层，晶体管密度已从155提升至2031年预计的400+ MTr/mm²。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• At the chip layer, LogicFolding has demonstrated that critical-path frequency, power efficiency, and density can continue to advance at a fixed device node.</p>
<p class="zh-text">• 在芯片层，LogicFolding证明关键路径频率、功耗效率和密度可以在固定器件节点下持续提升。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• At the system layer, Unified Bus and Hi-ONE have demonstrated that hundreds of microseconds of communication τ can be compressed to hundreds of nanoseconds.</p>
<p class="zh-text">• 在系统层，统一总线和Hi-ONE已经证明，数百微秒的通信τ可以被压缩到数百纳秒。</p>
</div>

<div class="bilingual-block">
<p class="en-text">• AI hardware integration is expected to grow more than 100× by 2035.</p>
<p class="zh-text">• AI硬件集成度预计到2035年增长超过100倍。</p>
</div>

<div class="bilingual-block">
<p class="en-text">The deeper claim, beyond any individual product, is methodological. τ scaling is the first scaling principle since Dennard to give the entire stack a shared optimization target. It signals to process technologists, circuit designers, architects, system engineers, and software teams that these communities are now optimizing the same quantity in identical units, and that improvements at any single layer must propagate to the system τ to count.</p>
<p class="zh-text">超越任何单一产品的更深论断是方法论层面的。τ缩放是自登纳德以来第一个为整个栈赋予共享优化目标的缩放原理。它向工艺技术专家、电路设计师、架构师、系统工程师和软件团队发出信号：这些群体现在正以相同的单位优化同一个量，且任何单一层面的改进必须传递到系统τ才算数。</p>
</div>

<div class="bilingual-block">
<p class="en-text">For a generation of engineers educated to treat "Moore's Law" as synonymous with "progress," this is a difficult transition. The geometric era has, in fact, concluded; denial of that fact is not a viable strategy. The era of acceleration through miniaturization is giving way to an era of acceleration through τ optimization across the multi-layered electronic system — and the companies, research groups, and ecosystems that adopt τ as the primary objective in the next six to ten years will determine the shape of computing in the decade thereafter.</p>
<p class="zh-text">对于一代被教育将"摩尔定律"等同于"进步"的工程师而言，这是一个艰难的转变。几何时代事实上已经终结；否认这一事实并非可行策略。通过微缩实现加速的时代，正让位于通过多层电子系统上的τ优化实现加速的时代——而在未来六到十年内采纳τ作为主要目标的公司、研究群体和生态系统，将决定此后十年计算的面貌。</p>
</div>

<div class="bilingual-block">
<p class="en-text">The next ten years of work are scoped. Many open questions remain, and no single organization can address them alone — the toolchain, the standards, the benchmarks, the device physics, and the economic models all require contributions from beyond any one company. This perspective is therefore intended as both a report from the field and an invitation.</p>
<p class="zh-text">未来十年的工作范围已经明确。许多开放问题仍然存在，没有任何单一组织能够独自解决——工具链、标准、基准测试、器件物理学和经济模型都需要超越任何一家公司的贡献。因此，本文既是一份来自一线的报道，也是一份邀请。</p>
</div>

## § Author & Acknowledgments / 作者与致谢

<div class="bilingual-block">
<p class="en-text">Tingbo He leads Huawei's semiconductor business. The team she directs has designed and brought to volume production 381 chips between 2020 and 2026 across mobile, AI, automotive, and infrastructure markets, and is the source of the τ scaling methodology and the LogicFolding, UnifiedBus, and Hi-ONE technologies described in this article.</p>
<p class="zh-text">何庭波领导华为的半导体业务。她所带领的团队在2020年至2026年间设计并量产交付了381颗芯片，涵盖移动、AI、汽车和基础设施市场，也是本文所述τ缩放方法论以及LogicFolding、UnifiedBus和Hi-ONE技术的来源。</p>
</div>

<div class="bilingual-block">
<p class="en-text">This perspective draws on six years of work by thousands of engineers across Huawei Semiconductor and its ecosystem of foundry, equipment, EDA, and system partners. The author thanks the customers whose patience made this work possible.</p>
<p class="zh-text">本文基于华为半导体及其代工厂、设备、EDA和系统合作伙伴生态系统中数千名工程师六年工作的积累。作者感谢那些以耐心使这项工作得以实现的客户。</p>
</div>

## § Further Reading / 延伸阅读

<div class="bilingual-block">
<p class="en-text">[1] G. E. Moore, "Cramming more components onto integrated circuits," Electronics, vol. 38, no. 8, pp. 114–117, Apr. 1965.</p>
<p class="zh-text">[1] G. E. Moore, "Cramming more components onto integrated circuits," Electronics, vol. 38, no. 8, pp. 114–117, Apr. 1965.</p>
</div>

<div class="bilingual-block">
<p class="en-text">[2] R. H. Dennard et al., "Design of ion-implanted MOSFETs with very small physical dimensions," IEEE J. Solid-State Circuits, vol. 9, no. 5, pp. 256–268, 1974.</p>
<p class="zh-text">[2] R. H. Dennard et al., "Design of ion-implanted MOSFETs with very small physical dimensions," IEEE J. Solid-State Circuits, vol. 9, no. 5, pp. 256–268, 1974.</p>
</div>

<div class="bilingual-block">
<p class="en-text">[3] J. L. Hennessy and D. A. Patterson, "A new golden age for computer architecture," Commun. ACM, vol. 62, no. 2, pp. 48–60, Feb. 2019.</p>
<p class="zh-text">[3] J. L. Hennessy and D. A. Patterson, "A new golden age for computer architecture," Commun. ACM, vol. 62, no. 2, pp. 48–60, Feb. 2019.</p>
</div>

<div class="bilingual-block">
<p class="en-text">[4] M. Horowitz, "Computing's energy problem (and what we can do about it)," ISSCC Dig. Tech. Papers, pp. 10–14, Feb. 2014.</p>
<p class="zh-text">[4] M. Horowitz, "Computing's energy problem (and what we can do about it)," ISSCC Dig. Tech. Papers, pp. 10–14, Feb. 2014.</p>
</div>

<div class="bilingual-block">
<p class="en-text">[5] International Roadmap for Devices and Systems (IRDS), 2023/2024 update.</p>
<p class="zh-text">[5] International Roadmap for Devices and Systems (IRDS), 2023/2024 update.</p>
</div>

<div class="bilingual-block">
<p class="en-text">[6] P. Batude et al., "3D sequential integration," IEEE J. Electron Devices Soc., vol. 3, no. 3, pp. 205–216, 2015.</p>
<p class="zh-text">[6] P. Batude et al., "3D sequential integration," IEEE J. Electron Devices Soc., vol. 3, no. 3, pp. 205–216, 2015.</p>
</div>
