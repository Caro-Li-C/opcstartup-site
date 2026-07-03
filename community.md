---
layout: default
title: 加入社群
permalink: /community/
---

<style>
  .community-page {
    font-family: 'Noto Sans SC', system-ui, sans-serif;
    background-color: #faf8f5;
    color: #1a1a1a;
    padding-top: 0;
  }
  .community-page .section-title {
    position: relative;
    display: inline-block;
  }
  .community-page .section-title::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 40px;
    height: 2px;
    background-color: #c9a87c;
  }
  .community-page .faq-content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease, padding 0.4s ease;
  }
  .community-page .faq-item.active .faq-content {
    max-height: 300px;
  }
  .community-page .faq-item.active .faq-icon {
    transform: rotate(45deg);
  }
  .community-page .group-card {
    transition: all 0.3s ease;
  }
  .community-page .group-card:hover {
    border-color: #c9a87c;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
  }
  .community-page .rule-card {
    transition: all 0.3s ease;
  }
  .community-page .rule-card:hover {
    border-color: #c9a87c;
  }
  .community-page .qr-card {
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  }
  .community-page .not-for-you {
    background: linear-gradient(135deg, #fdf6f0 0%, #faf8f5 100%);
  }
  .community-page .territory-notice {
    background: linear-gradient(135deg, #f5f0e8 0%, #faf8f5 100%);
  }
  .community-page .stat-number {
    font-size: 3rem;
    font-weight: 300;
    line-height: 1;
    color: #c9a87c;
  }
  .community-page .hero-pattern {
    background-image: radial-gradient(circle at 1px 1px, rgba(201,168,124,0.15) 1px, transparent 0);
    background-size: 40px 40px;
  }
  .community-page .divider-ornament {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .community-page .divider-ornament::before,
  .community-page .divider-ornament::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #e8e4df, transparent);
  }
  .community-page .tag-pill {
    display: inline-flex;
    align-items: center;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 12px;
    background: #f5f0e8;
    color: #8c8c8c;
  }
  .community-page .city-tag {
    transition: all 0.2s ease;
  }
  .community-page .city-tag:hover {
    background: #c9a87c;
    color: white;
    border-color: #c9a87c;
  }
  .community-page .tier-label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .community-page .tier-label .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #c9a87c;
  }
  .community-page .tier-label .count {
    color: #8c8c8c;
    font-weight: 400;
  }
</style>

<div class="community-page">

  <!-- Hero -->
  <section class="pt-16 pb-16 px-6 relative overflow-hidden">
    <div class="absolute inset-0 hero-pattern opacity-60"></div>
    <div class="max-w-4xl mx-auto relative">
      <div class="flex items-center gap-3 mb-8 text-sm">
        <span class="tag-pill">社群</span>
        <span style="color: #e8e4df;">|</span>
        <span class="text-muted">OPC</span>
        <span style="color: #e8e4df;">|</span>
        <span class="text-muted">一人公司</span>
        <span class="flex-1"></span>
        <span class="text-muted text-xs">2026-07-02</span>
      </div>

      <div class="flex items-start gap-8">
        <div class="flex-1">
          <h1 class="text-3xl md:text-4xl font-bold mb-3 leading-tight tracking-tight" style="color: #1a1a1a;">加入社群</h1>
          <p style="color: #c9a87c;" class="text-base mb-8">与全国超级个体建立真实连接</p>
        </div>
        <div class="hidden md:flex gap-6 text-center">
          <div>
            <div class="stat-number">39</div>
            <div class="text-xs text-muted mt-1">社群矩阵</div>
          </div>
          <div class="w-px" style="background: #e8e4df;"></div>
          <div>
            <div class="stat-number">18</div>
            <div class="text-xs text-muted mt-1">城市覆盖</div>
          </div>
        </div>
      </div>

      <div class="border-l-4 rounded-r-lg p-6 mt-4" style="border-color: #c9a87c; background: #f5f0e8;">
        <p class="text-muted leading-relaxed text-base">
          欢迎来到【OPC创业汇】。这里是一个OPC创业者之间建立真实连接的网络。我们相信：最好的资源不是信息，而是彼此信任的人。
        </p>
        <p class="text-muted leading-relaxed text-base mt-3">
          已有成员通过OPC创业汇找到联合创始人、达成战略合作、接到订单，也有成员成功入驻到契合的社区。
        </p>
      </div>
    </div>
  </section>

  <!-- 适合人群 -->
  <section class="py-12 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-10" style="color: #1a1a1a;">这里适合你，如果你</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-12">
        <div class="bg-white border rounded-lg p-6 relative overflow-hidden" style="border-color: #e8e4df;">
          <div class="absolute top-4 right-4" style="color: rgba(201,168,124,0.1);">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
          <div class="text-4xl font-light mb-4" style="color: rgba(201,168,124,0.3);">01</div>
          <p class="text-sm leading-relaxed" style="color: #1a1a1a;">正在<strong>独立运营自己的业务</strong></p>
        </div>
        <div class="bg-white border rounded-lg p-6 relative overflow-hidden" style="border-color: #e8e4df;">
          <div class="absolute top-4 right-4" style="color: rgba(201,168,124,0.1);">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          </div>
          <div class="text-4xl font-light mb-4" style="color: rgba(201,168,124,0.3);">02</div>
          <p class="text-sm leading-relaxed" style="color: #1a1a1a;">愿意<strong>分享真实经验</strong>，不只是成功</p>
        </div>
        <div class="bg-white border rounded-lg p-6 relative overflow-hidden" style="border-color: #e8e4df;">
          <div class="absolute top-4 right-4" style="color: rgba(201,168,124,0.1);">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
          </div>
          <div class="text-4xl font-light mb-4" style="color: rgba(201,168,124,0.3);">03</div>
          <p class="text-sm leading-relaxed" style="color: #1a1a1a;">想找到可以<strong>长期合作的伙伴</strong>，不只是客户</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 社群公约 -->
  <section class="py-12 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-10" style="color: #1a1a1a;">社群公约</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-12">
        <div class="rule-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">01</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">推文限额</h4>
              <p class="text-sm text-muted leading-relaxed">每人每周仅限分享一篇。好文一篇足矣，宁缺毋滥。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">02</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">AI内容</h4>
              <p class="text-sm text-muted leading-relaxed">禁止直接转发AI对话。请截取关键部分并附上你的解读。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">03</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">禁止霸屏</h4>
              <p class="text-sm text-muted leading-relaxed">请勿刷屏。各美其美，无需冗余；真知灼见，自会共鸣。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">04</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">产品推广</h4>
              <p class="text-sm text-muted leading-relaxed">允许自荐，每周一次。专注执行的你，不必重复推广。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">05</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">敏感话题</h4>
              <p class="text-sm text-muted leading-relaxed">涉及政治、宗教等敏感领域请谨慎发言，避免争议。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">06</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">尊重差异</h4>
              <p class="text-sm text-muted leading-relaxed">允许不同立场，反对无谓对立。理性探讨，对事不对人。</p>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 bg-white border rounded-lg p-5 text-center" style="border-color: #e8e4df;">
        <p class="text-sm text-muted">
          <span class="font-medium" style="color: #1a1a1a;">违规处理：</span>首次提醒，二次移出。
        </p>
      </div>
    </div>
  </section>

  <!-- 属地规则 -->
  <section class="py-12 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-10" style="color: #1a1a1a;">属地规则</h2>
      <div class="territory-notice border rounded-lg p-8 mt-12 max-w-3xl" style="border-color: #e8e4df;">
        <div class="flex items-start gap-3 mb-5">
          <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #c9a87c;">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <div>
            <p class="font-medium text-sm" style="color: #1a1a1a;">全国群仅限加入一个</p>
            <p class="text-xs text-muted mt-1">属地筛选 · 定期清理</p>
          </div>
        </div>
        <div class="space-y-3 text-sm text-muted leading-relaxed pl-13">
          <p>区域群仅面向属地成员或明确计划落地OPC业务的创业者开放。</p>
          <p>不符合属地条件的群友将被滚动请离，请大家理解并见谅。属地认定以实际属地或明确入驻意向为准，不接受"观望"或"未来可能"等模糊状态。</p>
          <p>入群后请修改备注：<span class="font-mono rounded text-xs px-2 py-0.5" style="color: #1a1a1a; background: rgba(26,26,26,0.05);">姓名/昵称-领域-所在区域</span>，24小时内未修改者将收到提醒。</p>
          <p>群内禁止无关广告、灌水及非属地城市的资源对接。违规即移，不另行通知。</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 不适合人群 -->
  <section class="py-12 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-10" style="color: #1a1a1a; opacity: 0.5;">这里不适合你，如果你</h2>
      <div class="not-for-you border rounded-lg p-8 mt-12 max-w-2xl" style="border-color: #e8e4df;">
        <ul class="space-y-4 text-muted text-sm">
          <li class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(26,26,26,0.05);">
              <span class="text-xs" style="color: rgba(26,26,26,0.3);">×</span>
            </div>
            <span>主要目的是推广产品</span>
          </li>
          <li class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(26,26,26,0.05);">
              <span class="text-xs" style="color: rgba(26,26,26,0.3);">×</span>
            </div>
            <span>不打算给别人提供任何价值</span>
          </li>
        </ul>
      </div>
    </div>
  </section>

  <!-- 社群矩阵 — 重新排布：全国群 → 重点城市群 → 区域群 → 省级群 -->
  <section class="py-12 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-10" style="color: #1a1a1a;">社群矩阵</h2>

      <div class="mt-12 space-y-14">

        <!-- 第一层级：全国群 -->
        <div>
          <div class="tier-label mb-4">
            <span class="dot"></span>
            <span style="color: #1a1a1a;">全国群</span>
            <span class="count">核心</span>
          </div>
          <div class="group-card bg-white border rounded-lg p-6" style="border-color: #e8e4df;">
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium text-base" style="color: #1a1a1a;">OPC创业汇 · 全国总群</span>
              <span class="text-xs rounded-full px-3 py-1" style="background: rgba(201,168,124,0.1); color: #c9a87c;">开放加入</span>
            </div>
            <p class="text-sm text-muted">覆盖全国OPC创业者，政策速递与资源对接。每人仅限加入一个全国群。</p>
          </div>
        </div>

        <!-- 第二层级：重点城市群 -->
        <div>
          <div class="tier-label mb-4">
            <span class="dot"></span>
            <span style="color: #1a1a1a;">重点城市群</span>
            <span class="count">11个</span>
          </div>
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">北京</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">上海</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">深圳</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">广州</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">杭州</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">香港</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">苏州</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">南京</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">成都</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">武汉</span>
            <span class="city-tag bg-white border rounded-full px-5 py-2.5 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">天津</span>
          </div>
          <p class="text-sm text-muted">重点城市群是OPC创业汇的核心阵地，覆盖创业密度最高的城市。当你的城市达到一定规模时，会开设专属城市群。</p>
        </div>

        <!-- 第三层级：区域群 -->
        <div>
          <div class="tier-label mb-4">
            <span class="dot" style="background: #c9a87c; opacity: 0.5;"></span>
            <span style="color: #1a1a1a;">区域群</span>
            <span class="count">5个</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <div class="group-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
              <div class="flex items-center justify-between mb-1">
                <span class="font-medium text-sm" style="color: #1a1a1a;">长三角区域群</span>
                <span class="text-xs rounded-full px-2 py-0.5" style="background: rgba(201,168,124,0.1); color: #c9a87c;">开放加入</span>
              </div>
              <p class="text-sm text-muted">上海、杭州、苏州、南京等</p>
            </div>
            <div class="group-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
              <div class="flex items-center justify-between mb-1">
                <span class="font-medium text-sm" style="color: #1a1a1a;">大湾区区域群</span>
                <span class="text-xs rounded-full px-2 py-0.5" style="background: rgba(201,168,124,0.1); color: #c9a87c;">开放加入</span>
              </div>
              <p class="text-sm text-muted">深圳、广州、香港等</p>
            </div>
            <div class="group-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
              <div class="flex items-center justify-between mb-1">
                <span class="font-medium text-sm" style="color: #1a1a1a;">京津冀区域群</span>
                <span class="text-xs rounded-full px-2 py-0.5" style="background: rgba(201,168,124,0.1); color: #c9a87c;">开放加入</span>
              </div>
              <p class="text-sm text-muted">北京、天津等</p>
            </div>
            <div class="group-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
              <div class="flex items-center justify-between mb-1">
                <span class="font-medium text-sm" style="color: #1a1a1a;">东北区域群</span>
                <span class="text-xs rounded-full px-2 py-0.5" style="background: rgba(201,168,124,0.1); color: #c9a87c;">开放加入</span>
              </div>
              <p class="text-sm text-muted">沈阳、大连、长春等</p>
            </div>
            <div class="group-card bg-white border rounded-lg p-5" style="border-color: #e8e4df;">
              <div class="flex items-center justify-between mb-1">
                <span class="font-medium text-sm" style="color: #1a1a1a;">川渝区域群</span>
                <span class="text-xs rounded-full px-2 py-0.5" style="background: rgba(201,168,124,0.1); color: #c9a87c;">开放加入</span>
              </div>
              <p class="text-sm text-muted">成都、重庆等</p>
            </div>
          </div>
          <p class="text-sm text-muted mt-4">区域群作为城市群的前置池，当你的城市尚未达到专属群规模时，先加入所属区域群。</p>
        </div>

        <!-- 第四层级：省级群 -->
        <div>
          <div class="tier-label mb-4">
            <span class="dot" style="background: #c9a87c; opacity: 0.3;"></span>
            <span style="color: #1a1a1a;">省级群</span>
            <span class="count">5个</span>
          </div>
          <div class="flex flex-wrap gap-2">
            <span class="city-tag bg-white border rounded-full px-4 py-2 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">安徽群</span>
            <span class="city-tag bg-white border rounded-full px-4 py-2 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">山东群</span>
            <span class="city-tag bg-white border rounded-full px-4 py-2 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">新疆群</span>
            <span class="city-tag bg-white border rounded-full px-4 py-2 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">河南群</span>
            <span class="city-tag bg-white border rounded-full px-4 py-2 text-sm cursor-default" style="border-color: #e8e4df; color: #1a1a1a;">江西群</span>
          </div>
          <p class="text-sm text-muted mt-4">省级群覆盖特定省份的OPC创业者，作为区域群的补充层级。</p>
        </div>

      </div>
    </div>
  </section>

  <!-- 装饰分隔 -->
  <div class="max-w-4xl mx-auto px-6">
    <div class="divider-ornament py-8">
      <span style="color: #c9a87c;" class="text-lg">◆</span>
    </div>
  </div>

  <!-- 二维码区 -->
  <section class="py-12 px-6">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="section-title text-xl font-medium mb-2" style="color: #1a1a1a;">扫码加入</h2>
      <p class="text-muted text-sm mt-10 mb-8">添加微信，备注「城市 + 行业」</p>

      <div class="max-w-sm mx-auto">
        <div class="qr-card bg-white border rounded-xl p-8" style="border-color: #e8e4df;">
          <div class="w-44 h-44 mx-auto rounded-lg flex items-center justify-center mb-5" style="background: #f5f5f5;">
            <div class="text-center">
              <svg class="w-10 h-10 mx-auto text-gray-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h2v-4H6v4zm6-6h2v-4h-2v4zm-6 0h2v-4H6v4zm12-6h2V4h-2v4zM6 10h2V4H6v6zm6-6h2V4h-2v4z"/>
              </svg>
              <span class="text-xs text-gray-400">微信二维码</span>
            </div>
          </div>
          <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">24小时内拉你入群</p>
          <p class="text-muted text-xs">审核通过后，按属地分配对应社群</p>
        </div>
        <p class="text-muted text-xs mt-8 italic">让每一次连接，都创造真正价值</p>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="py-12 px-6 pb-20">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-10" style="color: #1a1a1a;">常见问题</h2>

      <div class="mt-12 space-y-3 max-w-3xl">
        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">可以同时加入多个群吗？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">全国群仅限加入一个。区域/省级群每人限加入一个对应属地的群，不支持同时存在于多个区域群。</p>
          </div>
        </div>

        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">为什么需要审核？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">我们要交付信任的人。审核是为了确保每位成员都是真实的OPC创业者或从业者，维护社群质量。</p>
          </div>
        </div>

        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">社群是免费的吗？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">是的，所有社群均为免费加入。我们依靠成员自发贡献与价值交换维持运营，而非会员费。</p>
          </div>
        </div>

        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">我的城市没有专属群怎么办？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">可先加入所属区域群或全国总群。当所在城市成员达到一定规模时，我们会开设城市专属群。</p>
          </div>
        </div>
      </div>
    </div>
  </section>

</div>

<script>
  function toggleFaq(element) {
    const isActive = element.classList.contains('active');
    document.querySelectorAll('.community-page .faq-item').forEach(item => {
      item.classList.remove('active');
    });
    if (!isActive) {
      element.classList.add('active');
    }
  }
</script>
